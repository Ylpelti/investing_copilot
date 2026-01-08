import os
from datetime import UTC, date, datetime

import pandas as pd
import pytest
from fastapi.testclient import TestClient
from openai import OpenAI

from app.ai.adapters.openai_adapter import OpenAIAdapater
from app.ai.adapters.mock_adapter import MockAdapter
from app.ai.context.portfolio_context import PortfolioContextBuilder
from app.ai.prompts.portfolioprompt import PortfolioPrompt
from app.ai.pipelines.pipeline import ExplanationPipeline
from app.ai.pipelines.registry import PipelineRegistry
from app.ai.validation.basic_validation import BasicValidation
from app.ai.dependencies.dependencies import get_ai_service
from app.crud.transaction_crud import TransactionCrud
from app.crud.user_crud import UserCrud
from app.crud.portfolio_crud import PortfolioCrud
from app.crud.stock_crud import StockCrud
from app.main import app
from app.models.stock_price import StockPrice
from app.models.transaction import TransactionType
from app.security.dependencies import get_current_user
from app.schemas.transactions import TransactionCreate
from app.schemas.user import UserCreate
from app.schemas.portfolio import PortfolioCreate
from app.schemas.stock import StockCreate
from app.analytics.engine.portfolio_engine import PortfolioAnalyticsEngine
from app.analytics.engine.config import EngineConfig
from app.services.portfolio_explanation_service import PortfolioExplanationService
from app.ai.services.ai_explainer import AiExplainerService
from app.core.config import settings


class FakeCompletions:
    def __init__(self):
        self.last_args = None

    def create(self, model, messages):
        self.last_args = {"model": model, "messages": messages}
        message = type("Message", (), {"content": "Hello from OpenAI"})
        choice = type("Choice", (), {"message": message})
        return type("Response", (), {"choices": [choice]})


class FakeChat:
    def __init__(self):
        self.completions = FakeCompletions()


class FakeOpenAIClient:
    def __init__(self):
        self.chat = FakeChat()


class FakePortfolioExplanationService:
    def __init__(self, response_text="AI summary"):
        self.response_text = response_text
        self.called_with = None

    def explain_portfolio(self, txs, db):
        self.called_with = {"txs": txs, "db": db}
        return self.response_text


class TestPortfolioSummary:
    
        

    def test_pipeline_builds_prompt_and_validates(self):
        analytics_results = {
            "data": {"NAV": pd.Series([100.0, 110.0])},
            "returns": {"simple return": pd.Series([0.1])},
            "risk": {"max drawdown": 0.05, "volatility": 0.2, "sharpe ratio": 1.5},
        }
        pipeline = ExplanationPipeline(
            builder=PortfolioContextBuilder(),
            prompt=PortfolioPrompt(),
            llm=MockAdapter("Summary text."),
            validator=BasicValidation(),
        )

        result = pipeline.run(analytics_results)

        assert "Summary text." in result
        assert "not investment advice" in result.lower()

    def test_full_pipeline_user_portfolio_transaction_analytics_ai(self, test_db):
        user_crud = UserCrud(test_db)
        portfolio_crud = PortfolioCrud(test_db)
        stock_crud = StockCrud(test_db)
        transaction_crud = TransactionCrud(test_db)

        user = user_crud.create_user(
            UserCreate(username="pipeline_user", email="pipe@example.com", password="secret123")
        )
        portfolio = portfolio_crud.create_portfolio(
            PortfolioCreate(name="Pipeline Portfolio", description=None, user_id=user.id)
        )
        stock = stock_crud.create_stock(
            StockCreate(
                ticker="PIPE",
                isin="FI0000000001",
                name="Pipeline Oyj",
                close_price=10.0,
                sector="Tech",
                updated_at=datetime.now(UTC),
            )
        )

        prices = [
            StockPrice(stock_id=stock.id, date=date(2024, 1, 1), close_price=10.0),
            StockPrice(stock_id=stock.id, date=date(2024, 1, 2), close_price=11.0),
        ]
        test_db.add_all(prices)
        test_db.commit()

        tx = TransactionCreate(
            portfolio_id=portfolio.id,
            stock_id=stock.id,
            symbol=stock.ticker,
            type=TransactionType.BUY,
            quantity=10,
            price=10.0,
            timestamp=datetime(2024, 1, 1, tzinfo=UTC),
        )
        transaction_crud.ceate_transaction(tx, current_user_id=user.id)

        txs = transaction_crud.get_portfolio_transactions(
            portfolio_id=portfolio.id, current_user_id=user.id
        )

        pipeline = ExplanationPipeline(
            builder=PortfolioContextBuilder(),
            prompt=PortfolioPrompt(),
            llm=MockAdapter("Pipeline summary."),
            validator=BasicValidation(),
        )
        registry = PipelineRegistry({"portfolio_summary": pipeline})
        ai_service = AiExplainerService(registry)
        analytics_engine = PortfolioAnalyticsEngine(EngineConfig())
        explainer = PortfolioExplanationService(analytics_engine, ai_service)

        explanation = explainer.explain_portfolio(txs, test_db)

        assert "Pipeline summary." in explanation
        assert "not investment advice" in explanation.lower()

    def test_portfolio_explain_endpoint_uses_owned_portfolio(
        self, test_db, test_user, test_portfolio, monkeypatch
    ):
        original_get_transactions = TransactionCrud.get_portfolio_transactions

        def patched_get_transactions(self, portfolio_id, current_user=None, current_user_id=None):
            user_id = current_user_id
            if user_id is None:
                user_id = getattr(current_user, "id", current_user)
            return original_get_transactions(self, portfolio_id, user_id)

        monkeypatch.setattr(
            TransactionCrud, "get_portfolio_transactions", patched_get_transactions
        )

        fake_service = FakePortfolioExplanationService()

        app.dependency_overrides[get_current_user] = lambda: test_user
        app.dependency_overrides[get_ai_service] = lambda: fake_service
        client = TestClient(app)
        try:
            response = client.post(f"/portfolios/{test_portfolio.id}/explain")
        finally:
            app.dependency_overrides.clear()

        assert response.status_code == 200
        body = response.json()
        assert body["portfolio_id"] == test_portfolio.id
        assert body["explanation"] == "AI summary"
        assert fake_service.called_with is not None
        print(f"AI output: {body['explanation']}")
