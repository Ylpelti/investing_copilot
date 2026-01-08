from app.ai.adapters.base_adapter import LLMAdapter
from app.core.config import settings
from app.ai.adapters.factory import create_llm_adapter
from fastapi import Depends
from app.ai.pipelines.pipeline import ExplanationPipeline
from app.ai.services.ai_explainer import AiExplainerService

from app.ai.context.portfolio_context import PortfolioContextBuilder
from app.ai.prompts.portfolioprompt import PortfolioPrompt
from app.ai.validation.basic_validation import BasicValidation

from app.ai.pipelines.registry import PipelineRegistry



def get_llm_adapter() -> LLMAdapter:
    return create_llm_adapter(settings)

def get_ai_service(llm: LLMAdapter = Depends(get_llm_adapter)):
    portfolio_summary_pipeline = ExplanationPipeline(
        builder=PortfolioContextBuilder(),
        prompt=PortfolioPrompt(),
        llm=llm,
        validator=BasicValidation()
    )

    registry = PipelineRegistry({
        "portfolio_summary" : portfolio_summary_pipeline
    })

    return AiExplainerService(registry)