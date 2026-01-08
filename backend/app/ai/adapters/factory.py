from openai import OpenAI
from app.ai.adapters.base_adapter import LLMAdapter
from app.schemas.llm_provider import LLMProvider
from app.ai.adapters.mock_adapter import MockAdapter
from app.core.config import Settings
from app.ai.adapters.openai_adapter import OpenAIAdapater

def create_llm_adapter(settings:Settings) -> LLMAdapter:
    if settings.llm_provider == LLMProvider.OPENAI:
        client = OpenAI(api_key=settings.openai_api_key)
        return OpenAIAdapater(client)
    if settings.llm_provider == LLMProvider.MOCK:
        return MockAdapter()
    raise ValueError("LLM provider not available")