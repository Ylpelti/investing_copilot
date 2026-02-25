from datetime import UTC, datetime
from types import SimpleNamespace

import pandas as pd

from app.ai.adapters.mock_adapter import MockAdapter
from app.ai.context.portfolio_context import PortfolioContextBuilder
from app.ai.pipelines.pipeline import ExplanationPipeline
from app.ai.prompts.portfolioprompt import PortfolioPrompt
from app.ai.validation.basic_validation import BasicValidation
from app.services.portfolio.dependencies import get_portfolio_explanation_service
from app.services.portfolio.portfolio_explanation_service import PortfolioExplanationService


class FakeTxService:
    def __init__(self, txs):
        self.txs = txs

    def get_portfolio_transactions(self, portfolio_id):
        return self.txs


class FakeAiService:
    def __init__(self, message="AI summary"):
        self.message = message
        self.last_payload = None

    def explain(self, payload, kind):
        self.last_payload = {"payload": payload, "kind": kind}
        return self.message


class FakePortfolioExplanationService:
    def __init__(self, response_text="AI summary"):
        self.response_text = response_text
        self.called_with = None

    def explain_portfolio(self, portfolio_id):
        self.called_with = portfolio_id
        return self.response_text


class FakeAnalyticsEngine:
    def compute(self, txs, db):
        nav = pd.Series([100.0, 110.0], index=pd.date_range("2024-01-01", periods=2, tz="UTC"))
        simple_ret = pd.Series([0.1], index=nav.index[1:])
        cum_ret = pd.Series([0.1], index=nav.index[1:])
        log_ret = pd.Series([0.0953102], index=nav.index[1:])
        risk = {"max drawdown": -0.01, "volatility": 0.2, "sharpe ratio": 1.5}
        return SimpleNamespace(nav=nav, simple_ret=simple_ret, cum_ret=cum_ret, log_ret=log_ret, risk=risk)


def test_pipeline_builds_prompt_and_validates():
    analytics_results = {
        "nav": pd.Series([100.0, 110.0]),
        "simple return": pd.Series([0.1]),
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


def test_portfolio_explanation_service_calls_ai_with_metrics(test_db, test_stock):
    txs = [
        SimpleNamespace(
            portfolio_id=1,
            stock_id=test_stock.id,
            quantity=10,
            price=10.0,
            type="BUY",
            timestamp=datetime(2024, 1, 1, tzinfo=UTC),
        )
    ]
    ai = FakeAiService("Pipeline summary.")
    service = PortfolioExplanationService(
        analytics_engine=FakeAnalyticsEngine(),
        ai_explainer=ai,
        db=test_db,
        tx_service=FakeTxService(txs),
    )

    explanation = service.explain_portfolio(portfolio_id=1)
    assert "Pipeline summary." in explanation
    assert ai.last_payload is not None
    assert ai.last_payload["kind"] == "portfolio_summary"


def test_portfolio_explain_endpoint_with_override(client, app):
    fake_service = FakePortfolioExplanationService("AI summary")
    app.dependency_overrides[get_portfolio_explanation_service] = lambda: fake_service
    try:
        response = client.post("/api/v1/portfolios/1/explain")
    finally:
        app.dependency_overrides.pop(get_portfolio_explanation_service, None)
    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == 1
    assert body["explanation"] == "AI summary"
    assert fake_service.called_with == 1
