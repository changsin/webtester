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

from src.util import serialize
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
    def __init__(self, browser_options):
        self.browser_options = browser_options

        # TODO: support custom xpath_patterns
        self.xpath_patterns = None

    def __iter__(self):
        yield from {
            "browser_options": self.browser_options
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

    @staticmethod
    def from_json(path):
        options = util.load_json_file(path)
        browser_options = util.safe_get_dict_item(options, BROWSER_OPTIONS)
        return Options(browser_options)
