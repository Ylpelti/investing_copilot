import pandas as pd
import os
import pytest
from fastapi.testclient import TestClient
from openai import OpenAI

from app.ai.adapters.openai_adapter import OpenAIAdapater
from app.ai.adapters.mock_adapter import MockAdapter
from app.ai.context.portfolio_context import PortfolioContextBuilder
from app.ai.prompts.portfolioprompt import PortfolioPrompt
from app.ai.pipelines.pipeline import ExplanationPipeline
from app.ai.validation.basic_validation import BasicValidation
from app.ai.dependencies.dependencies import get_ai_service
from app.crud.transaction_crud import TransactionCrud
from app.main import app
from app.security.dependencies import get_current_user
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
    @pytest.mark.integration
    def test_openai_live_call_outputs_text(self):
        api_key = settings.openai_api_key
        if not api_key:
            pytest.skip("OPENAI_API_KEY not set; skipping live OpenAI call")
        client = OpenAI(api_key=api_key)
        adapter = OpenAIAdapater(client)
        messages = [{"role": "user", "content": "Say hello in one short sentence."}]

        result = adapter.generate(messages)

        print(f"AI output: {result}")
        assert isinstance(result, str)
        assert result.strip()

    def test_openai_adapter_calls_chat_completions(self):
        client = FakeOpenAIClient()
        adapter = OpenAIAdapater(client)
        messages = [{"role": "user", "content": "Hello"}]

        result = adapter.generate(messages)

        assert result == "Hello from OpenAI"
        assert client.chat.completions.last_args["model"] == "gpt-4o-mini"
        assert client.chat.completions.last_args["messages"] == messages

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
