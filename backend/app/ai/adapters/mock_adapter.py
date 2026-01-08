from typing import Dict, List
from app.ai.adapters.base_adapter import LLMAdapter


class MockAdapter(LLMAdapter):

    def __init__(self, fixed_response: str = "Mock explanation."):
        self.fixed_response = fixed_response

    def generate(self, message: List[Dict[str, str]]) -> str:
        return self.fixed_response