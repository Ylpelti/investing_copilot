class BasePromptTemplate:
    system_prompt: str
    user_prompt: str

    def render(self, context: dict) -> list[dict]:
        return [
            {"role": "system", "content": self.system_prompt },
            {
                "role": "user", "content":self.user_prompt.format(**context)
            }
        ]