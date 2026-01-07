import logging

class BaseAnalyticsEngine:
    def __init__(self, config):
        self.config = config
        self.cache = {}
        self.logger = logging.getLogger(self.__class__.__name__)

    def compute(self, *args,  **kvargs):
        raise NotImplementedError("Subclasses must implement compute()")
