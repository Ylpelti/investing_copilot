from app.ai.validation.base import BaseValidation

class BasicValidation(BaseValidation):
    def validate(self, text: str) -> str:
        text = (text or " ").strip()

        if not text:
            text = "Couldn't generate an explanation for you"

        disclaimer = "\n\nNote: This explanation is informational and not investment advice."
        if "not investment advice" not in text.lower():
            text += disclaimer

        return text