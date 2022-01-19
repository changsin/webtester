from src.model.node.node import NodeStatus
from src.util import url_util
from src.util.logger import get_logger
from .pattern_matcher import PatternMatcher

logger = get_logger(__name__)

blacklist_targets = {
    "mailto",
    "tel"
}


class BlacklistPattern(PatternMatcher):
    def __init__(self, driver, options):
        super(BlacklistPattern, self).__init__(driver, options)

    def accept(self, node):
        return node.status == NodeStatus.Parsed

    def apply(self, node):
        if url_util.is_domain_whitelisted(self.options.wl_domains, node.target):
            node.status = NodeStatus.Parsed

        # TODO: make this as a separate pattern
        if not url_util.is_same_domain(self.driver.current_url, node.target):
            node.status = NodeStatus.Filtered
            return

        for blacklist_target in blacklist_targets:
            if node.target and node.target.startswith(blacklist_target):
                node.status = NodeStatus.Filtered
                return

        if self.options.blacklist_labels:
            if node.label and node.label in self.options.blacklist_labels:
                node.status = NodeStatus.Filtered
