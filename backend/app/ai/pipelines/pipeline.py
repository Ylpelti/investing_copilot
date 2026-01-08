from dataclasses import dataclass
from typing import Dict, Any

from app.ai.context.base_context_builder import BaseContext
from app.ai.prompts.prompt_template import BasePromptTemplate
from app.ai.adapters.base_adapter import LLMAdapter
from app.ai.validation.base import BaseValidation

@dataclass(frozen=True)
class ExplanationPipeline:
    builder: BaseContext
    prompt: BasePromptTemplate
    llm: LLMAdapter
    validator: BaseValidation

    def run(self, analytic_results: Dict[str, Any]):
        context = self.builder.build(analytic_results)
        message = self.prompt.render(context)
        response_raw = self.llm.generate(message)
        response = self.validator.validate(response_raw)
        return response


