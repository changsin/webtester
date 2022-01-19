from abc import ABC

from src.util.logger import get_logger

logger = get_logger(__name__)


class PatternMatcher(ABC):
    def __init__(self, driver, options):
        self.driver = driver
        self.options = options

    def accept(self, node):
        raise NotImplemented

    def find_constraints(self, node):
        raise NotImplemented

    def apply(self, node):
        if self.accept(node):
            return self.find_constraints(node)
