import re

from src.util.logger import get_logger
from . import util

logger = get_logger(__name__)


def get_absolute_xpath(element):
    """
    get the absolute path of the element
    inspired by
    https://stackoverflow.com/questions/18510576/find-an-element-by-text-and-get-xpath-selenium-webdriver-junit
    :param element:
    :return: absolute xpath of the element
    """
    parents = element.find_elements_by_xpath("./ancestor::*")
    size = len(parents)

    path = ""
    current = element

    # traverse up the html tree
    for idx in range(size - 1, -1, -1):
        tag = current.tag_name
        siblings = current.find_elements_by_xpath("./preceding-sibling::" + tag)
        level = len(siblings) + 1
        path = "/{}[{}]{}".format(tag, level, path)
        current = current.find_element_by_xpath("./parent::*")

    return "/" + current.tag_name + path


def get_relative_xpath(element):
    """
    relative xpath of the element based on one of the id (its own or parent's)
    :param element:
    :return: relative xpath of the element
    """
    parents = element.find_elements_by_xpath("./ancestor::*")
    size = len(parents)

    path = ""
    current = element

    # traverse up the html tree
    for idx in range(size - 1, -1, -1):
        tag = current.tag_name
        element_id = current.get_attribute("id")
        if element_id:
            tag_id = "//*[@id=\'" + element_id + "\']"
            return tag_id + path

        siblings = current.find_elements_by_xpath("./preceding-sibling::" + tag)
        level = len(siblings) + 1
        path = "/{}[{}]{}".format(tag, level, path)
        current = current.find_element_by_xpath("./parent::*")

    return "/" + current.tag_name + path


def find_tag_list_parent_xpath(xpath, tag_name):
    """
    find /ul/li[\\d]/a pattern - this seems to be a very common way to make menu items
    Returns the parent xpath of the <a tag list.
    Usually, when the mouse is moved over the parent node, the a tag element is visible and clickable.
    :param xpath:
    :param tag_name:
    :return:
    """
    matched = re.search("/ul(\\[\\d\\])*/li\\[\\d\\]/" + tag_name, xpath)
    if matched:
        start, end = matched.span()
        parent_xpath = xpath[:start]
        logger.info("  found list parent xpath (%s)", parent_xpath)
        return parent_xpath
    else:
        return None


def to_regex(expression):
    """
    replaces expression (usually xpath expression to regex)
    """
    to_replace = {
        "/": "\\/",
        "*": "\\*",
        "@": "\\@",
        "\"": "\\\"",
        "[": "\\[",
        "]": "\\]"
    }

    for k, v in to_replace.items():
        expression = expression.replace(k, v)

    return expression


def is_xpath_selected(filters, xpath):
    """
    a filter consists of two parts: (scope_pattern, select_pattern)
    the scope_pattern prescribes the scope: the set of xpaths that this pattern is applicable to - e.g., /div/div/ul/li
    the select_pattern decides exactly which elements are to be selected for crawling
    :param filters: a set of filter pairs
    :param xpath: xpath that we want to test against
    :return:
    """
    if not filters:
        return True

    xpath_dict = util.safe_get_dict_item(filters, "xpath")
    if xpath_dict:
        for scope_pattern, select_pattern in xpath_dict.items():
            in_scope = re.search(scope_pattern, xpath)
            if in_scope:
                if re.search(select_pattern, xpath):
                    return True
                else:
                    return False

    return True


def is_xpath_popup(filters, xpath):
    """
    filters contains regex that match popup xpaths
    :param filters: a set of filter pairs
    :param xpath: xpath that we want to test against
    :return:
    """
    if not filters:
        return False

    xpath_dict = util.safe_get_dict_item(filters, "popup")
    if xpath_dict:
        for popup_pattern, action in xpath_dict.items():
            is_popup = re.search(popup_pattern, xpath)
            if is_popup:
                return True
