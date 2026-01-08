from typing import Dict
from .pipeline import ExplanationPipeline

class PipelineRegistry:
    def __init__(self, pipelines: Dict[str, ExplanationPipeline]):
        self._pipelines = pipelines

    def get(self, kind: str) -> ExplanationPipeline:
        if kind not in self._pipelines:
            raise KeyError(f"Unknown explanation kind: {kind}")
        return self._pipelines[kind]
