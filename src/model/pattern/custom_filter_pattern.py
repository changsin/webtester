from src.model.node.node import NodeStatus
from src.util import xpath_util
from src.util.logger import get_logger
from .pattern_matcher import PatternMatcher

logger = get_logger(__name__)


class CustomFilterPattern(PatternMatcher):
    def __init__(self, driver, options):
        super(CustomFilterPattern, self).__init__( driver, options)

    def accept(self, node):
        return self.options.filters and node.status == NodeStatus.Parsed

    def apply(self, node):
        if not xpath_util.is_xpath_selected(self.options.filters, node.xpath):
            logger.info("  *filtered (%s)", node)
            node.status = NodeStatus.FilteredCustom

