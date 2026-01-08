class AiExplainerService:
    def __init__(
            self,
            context_builder,
            prompt_template,
            llm_adapter,
            basic_validation
    ):
        self.contex_builder = context_builder
        self.prompt_template = prompt_template
        self.llm_adapter = llm_adapter
        self.basic_validation = basic_validation

    def explain(self, analytics):
        context = self.contex_builder.build(analytics)

        message = self.prompt_template.render(context)

        response_raw = self.llm_adapter.generate(message)

        response = self.basic_validation.validate(response_raw)

        return response