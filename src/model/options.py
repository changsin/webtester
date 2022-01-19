"""
Copyright (C) 2020 TestWorks Inc.

2020-03-05: changsin@ created as a POC

  Options specify custom behavior for a web site.
    - blacklist_targets: targets which we don't want to crawl
    - blacklist_values: elements we don't want to crawl
    - constraints: For a given url, specify the sequence of steps that must be followed:
        e.g., a login page must have steps:
        1. Enter a user id
        2. Type the password
        3. Press Enter or click submit button
"""
import json

from src.model.node.node import Node
from src.util import serialize
from src.util import url_util
from src.util import util
from src.util.logger import get_logger

logger = get_logger(__name__)

BROWSER_OPTIONS = 'browser_options'
WHITELIST_DOMAINS = 'whitelist_domains'
BLACKLIST_LABELS = 'blacklist_labels'
HAMBURGER_MENU = 'hamburger_menu'
PATTERN_MATCHERS = "pattern_matchers"
FILTERS = 'filters'
PRE_CONSTRAINTS = 'pre_constraints'
POST_CONSTRAINTS = 'post_constraints'

DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080


class Options:
    """
    filters - (xpath regular expression, action)

    """
    def __init__(self, browser_options, wl_domains, bl_labels, hamburger_menu,
                 pattern_matchers, filters, pre_constraints, post_constraints):
        self.browser_options = browser_options
        self.wl_domains = wl_domains
        self.blacklist_labels = bl_labels
        self.hamburger_menu = hamburger_menu
        self.pattern_matchers = pattern_matchers
        self.filters = filters
        self.pre_constraints = pre_constraints
        self.post_constraints = post_constraints

        # TODO: support custom xpath_patterns
        self.xpath_patterns = None

    def __iter__(self):
        yield from {
            "browser_options": self.browser_options,
            "whitelist_domains": self.wl_domains and list(self.wl_domains),
            "blacklist_labels": self.blacklist_labels and list(self.blacklist_labels),
            "hamburger_menu": self.hamburger_menu,
            "pattern_matchers": self.pattern_matchers and list(self.pattern_matchers),
            "filters": self.filters,
            "pre_constraints": self.pre_constraints,
            "post_constraints": self.post_constraints,
        }.items()

    def __str__(self):
        return json.dumps(dict(self), default=serialize.default, ensure_ascii=False)

    def is_mobile(self):
        width = util.safe_get_dict_item(self.browser_options, "width")
        height = util.safe_get_dict_item(self.browser_options, "height")
        return self.browser_options and width and height

    def get_max_width(self):
        width = util.safe_get_dict_item(self.browser_options, "width")
        if width:
            return width
        else:
            return DEFAULT_WIDTH

    def get_max_height(self):
        height = util.safe_get_dict_item(self.browser_options, "height")
        if height:
            return height
        else:
            return DEFAULT_HEIGHT

    def to_json(self):
        return self.__str__()

    def get_xpath_patterns(self, node_type, default_patterns):
        """
        return xpath_patterns based on the element_type
        :param node_type: button, input, link, select_option
        :param default_patterns:
        :return:
        """
        if self.xpath_patterns:
            patterns = util.safe_get_dict_item(self.xpath_patterns, node_type.value)
            if patterns:
                return patterns

        return default_patterns

    @staticmethod
    def from_json(path):
        def set_constraints(constraints, key, constraints_dict):
            """
            deserialize constraints to pre- or post-constraints.
            The catch is to support both serialized constraints from Watts program (in strings)
             as well as user-written constraints (in dict)
            :param constraints:
            :param key:
            :param constraints_dict:
            :return:
            """
            if constraints_dict and isinstance(constraints_dict[0], str):
                # if the input is string, convert it to a node object
                constraints[key] = [Node.from_json(json.loads(cn)) for cn in constraints_dict]
            else:
                constraints[key] = [Node.from_json(item) for item in constraints_dict]

        options = util.load_json_file(path)

        browser_options = util.safe_get_dict_item(options, BROWSER_OPTIONS)

        wl_domains = util.safe_get_dict_item(options, WHITELIST_DOMAINS)
        if wl_domains:
            wl_domains = set(wl_domains)

        bl_labels = util.safe_get_dict_item(options, BLACKLIST_LABELS)
        if bl_labels:
            bl_labels = set(bl_labels)

        hamburger_menu = util.safe_get_dict_item(options, HAMBURGER_MENU)
        if hamburger_menu:
            hamburger_menu = Node.from_json(hamburger_menu)

        pattern_matchers = util.safe_get_dict_item(options, PATTERN_MATCHERS)
        if pattern_matchers:
            # NB: be sure to preserve the order
            pattern_matchers = list(pattern_matchers)

        filters = util.safe_get_dict_item(options, FILTERS)

        pre_constraints_dict = util.safe_get_dict_item(options, PRE_CONSTRAINTS)
        pre_constraints = dict()
        if pre_constraints_dict:
            [set_constraints(pre_constraints, k, pre_constraints_dict[k])
                for k in pre_constraints_dict]

        post_constraints_dict = util.safe_get_dict_item(options, POST_CONSTRAINTS)
        post_constraints = dict()
        if post_constraints_dict:
            [set_constraints(post_constraints, k, post_constraints_dict[k])
                for k in post_constraints_dict]

        return Options(browser_options, wl_domains, bl_labels, hamburger_menu,
                       pattern_matchers, filters, pre_constraints, post_constraints)

    # apply constraints to actionable_nodes by replacing the parsed values with the pre-specified ones
    def apply_constraints(self, actionable_nodes):
        for node in actionable_nodes:
            constraint_nodes = util.safe_get_dict_item(self.post_constraints, node.get_key())
            if constraint_nodes:
                for cn in constraint_nodes:
                    if url_util.is_same_page(node.url, cn.url) and node.xpath == cn.xpath:
                        node.value = cn.value

        return actionable_nodes
