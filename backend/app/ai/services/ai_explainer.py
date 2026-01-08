from typing import Dict, Any
from app.ai.pipelines.registry import PipelineRegistry

class AiExplainerService:
    def __init__(self, registry: PipelineRegistry):
        self.registry = registry

    def explain(self, analytic_results: Dict[str, Any], kind: str) -> str:
        pipeline = self.registry.get(kind)
        return pipeline.run(analytic_results)
