from typing import Dict, List
from app.ai.adapters.base_adapter import LLMAdapter


class OpenAIAdapater(LLMAdapter):

    def __init__(self, client):
        self.client = client

    def generate(self, message: List[Dict[str, str]]) -> str:
        res = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=message
        )
        return res.choices[0].message.content