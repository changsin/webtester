from src.metrics.page_metrics import PageMetrics
from src.model.node.node import NodeStatus
from src.model.pattern.a_tag_list_pattern import ATagListPattern
from src.model.pattern.blacklist_pattern import BlacklistPattern
from src.model.pattern.custom_filter_pattern import CustomFilterPattern
from src.model.pattern.hamburger_menu_pattern import HamburgerMenuPattern
from src.util.decorators import calc_time
from src.util.logger import get_logger
from .analyzer import Analyzer

logger = get_logger(__name__)


class PageAnalyzer(Analyzer):
    def __init__(self, driver, options):
        super(PageAnalyzer, self).__init__(driver, options)
        self.page_metrics = []
        self.analyzers = [
            Analyzer(driver, options)
        ]

        # default patterns
        self.pattern_matchers = [
            ATagListPattern(driver, options),
            CustomFilterPattern(driver, options),
            BlacklistPattern(driver, options),
        ]

        # TODO: this is a hack to make it backward compatible.
        if options.pattern_matchers:
            self.pattern_matchers.clear()

            self.pattern_matchers = list()
            for pm in options.pattern_matchers:
                if pm == "HamburgerMenuPattern":
                    self.pattern_matchers.append(HamburgerMenuPattern(driver, options))
                if pm == "ATagListPattern":
                    self.pattern_matchers.append(ATagListPattern(driver, options))
                if pm == "CustomFilterPattern":
                    self.pattern_matchers.append(CustomFilterPattern(driver, options))
                if pm == "BlacklistPattern":
                    self.pattern_matchers.append(BlacklistPattern(driver, options))

    @calc_time
    def analyze(self):
        """
        start of the main function
        """
        actionable_nodes = list()
        node_metrics_dict = dict()

        for analyzer in self.analyzers:
            nodes, node_metrics = analyzer.analyze()
            for node in nodes:
                if not node.is_within_view(self.options.get_max_width()):
                    node.status = NodeStatus.Hidden

                actionable_nodes.append(node)

            node_metrics_dict = node_metrics.__dict__
            logger.info(" found (%s)", node_metrics.__dict__)

        self.options.apply_constraints(actionable_nodes)

        self.apply_patterns(actionable_nodes)

        [logger.info("%s, %s, %s, %s, %s", n.tag, n.status, n.label, n.target, n.xpath) for n in actionable_nodes]

        # hidden_nodes can become visible once certain conditions are met so try both types
        return actionable_nodes, PageMetrics(node_metrics_dict), self.options

    def apply_patterns(self, nodes):
        for node in nodes:
            for pattern_matcher in self.pattern_matchers:
                if pattern_matcher.accept(node):
                    pattern_matcher.apply(node)

        return self.options
