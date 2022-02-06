from src.model.node.node import NodeStatus
from src.util import util
from src.util.logger import get_logger
from .pattern_matcher import PatternMatcher

logger = get_logger(__name__)


class HamburgerMenuPattern(PatternMatcher):
    def __init__(self, driver, options):
        super(HamburgerMenuPattern, self).__init__(driver, options)

    def accept(self, node):
        return self.options and self.options.hamburger_menu \
            and (node.rect['x'] <= 0 or node.rect['x'] > self.options.get_max_width())

    def apply(self, node):
        hamburger_menu_node = self.options.hamburger_menu

        try:
            el = self.driver.find_element_by_xpath(hamburger_menu_node.xpath)
        except:
            return False

        if hamburger_menu_node.parse(el):
            actions = util.safe_get_dict_item(self.options.pre_constraints, node.get_key())
            if actions:
                actions.insert(0, hamburger_menu_node)
            else:
                self.options.pre_constraints[node.get_key()] = [hamburger_menu_node]
            node.status = NodeStatus.Parsed
