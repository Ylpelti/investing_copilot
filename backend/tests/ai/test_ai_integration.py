import pytest
from openai import OpenAI
from openai import APIConnectionError

from app.ai.adapters.openai_adapter import OpenAIAdapater
from app.ai.context.portfolio_context import PortfolioContextBuilder
from app.ai.prompts.portfolioprompt import PortfolioPrompt
from app.ai.pipelines.pipeline import ExplanationPipeline
from app.ai.validation.basic_validation import BasicValidation
from app.core.config import settings
import pandas as pd


@pytest.mark.integration
def test_ai_pipeline_real_openai_call():
    if not settings.openai_api_key:
        pytest.skip("OPENAI_API_KEY not set")

    analytics_results = {
        "nav": pd.Series([100, 110]),
        "simple return": pd.Series([0.10]),
        "risk": {
            "max drawdown": 0.05,
            "volatility": 0.2,
            "sharpe ratio": 1.5,
        },
    }

    client = OpenAI(api_key=settings.openai_api_key)
    adapter = OpenAIAdapater(client)

    pipeline = ExplanationPipeline(
        builder=PortfolioContextBuilder(),
        prompt=PortfolioPrompt(),
        llm=adapter,
        validator=BasicValidation(),
    )

    try:
        result = pipeline.run(analytics_results)
    except APIConnectionError:
        pytest.skip("OpenAI endpoint not reachable in current environment")

    assert isinstance(result, str)
    assert len(result.strip()) > 20
