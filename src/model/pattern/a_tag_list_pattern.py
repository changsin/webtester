from src.model.node.node import Action, NodeStatus, Node
from src.util import util
from src.util.logger import get_logger
from src.util.xpath_util import find_tag_list_parent_xpath
from .pattern_matcher import PatternMatcher

logger = get_logger(__name__)


class ATagListPattern(PatternMatcher):
    def __init__(self, driver, options):
        super(ATagListPattern, self).__init__(driver, options)

    def accept(self, node):
        return node.xpath.find("/ul[")

    def apply(self, node):
        parent_nodes = list()

        parent_node = self.find_actionable_parent(node)
        if parent_node:
            parent_nodes.insert(0, parent_node)
            # find all actionable parents iteratively
            while parent_node:
                parent_node = self.find_actionable_parent(parent_node)
                if parent_node:
                    parent_nodes.insert(0, parent_node)

            actions = util.safe_get_dict_item(self.options.pre_constraints, node.get_key())
            if actions:
                actions.extend(parent_nodes)
            else:
                actions = parent_nodes
                self.options.pre_constraints[node.get_key()] = actions

    def find_actionable_parent(self, node):
        tag_name = node.tag
        if not tag_name:
            tag_name = ""

        parent_xpath = find_tag_list_parent_xpath(node.xpath, tag_name)
        if parent_xpath:
            # create a new node for mouse move or click
            parent_node = Node(node.url)

            if self.options.is_mobile():
                # TODO: hard-coded for Atomy mobile site as the parent node might be /a[1]
                tag_name = "button"

            parent_xpath = parent_xpath + "/" + tag_name

            try:
                parent_element = self.driver.find_element_by_xpath(parent_xpath)
            except:
                return False

            if parent_node.parse(parent_element):
                if not self.options.is_mobile():
                    parent_node.action = Action.MOUSE_MOVE

                node.status = NodeStatus.Parsed

                return parent_node
