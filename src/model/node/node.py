"""
Copyright (C) 2020 TestWorks Inc.

2020-03-05: changsin@ created as a POC

"""
import json
from abc import ABC
from enum import Enum

from selenium.common import exceptions

from src.metrics.page_metrics import PageMetrics
from src.util import selenium_util
from src.util import util
from src.util import xpath_util
from src.util.decorators import handle_selenium_exceptions
from src.util.logger import get_logger

logger = get_logger(__name__)


class Action(Enum):
    OPEN = "open"
    CLICK = "click"
    TYPE = "type"
    MOUSE_MOVE = "mouse_move"
    NONE = "none"


class NodeStatus(Enum):
    Parsed = "Parsed"
    Filtered = "Filtered"
    FilteredCustom = "FilteredCustom"
    FilteredDuplicate = "FilteredDuplicate"
    Actionable = "Actionable"
    Hidden = "Hidden"

    ElementNotFoundException = "ElementNotFoundException"
    ActionException = "ActionException"

    # Selenium exceptions
    UnexpectedAlertPresentException = "UnexpectedAlertPresentException"
    StaleElementReferenceException = "StaleElementReferenceException"
    NoSuchElementException = "NoSuchElementException"
    ElementNotInteractableException = "ElementNotInteractableException"
    ElementClickInterceptedException = "ElementClickInterceptedException"
    TimeoutException = "TimeoutException"
    UnknownException = "UnknownException"

    @staticmethod
    def from_exception(ex):
        exc = {
            exceptions.UnexpectedAlertPresentException: NodeStatus.UnexpectedAlertPresentException,
            exceptions.StaleElementReferenceException: NodeStatus.StaleElementReferenceException,
            exceptions.NoSuchElementException: NodeStatus.NoSuchElementException,
            exceptions.ElementNotInteractableException: NodeStatus.ElementNotInteractableException,
            exceptions.ElementClickInterceptedException: NodeStatus.ElementClickInterceptedException,
            exceptions.TimeoutException: NodeStatus.TimeoutException
        }.get(ex)

        if not exc:
            exc = NodeStatus.UnknownException
        return exc


# maximum x coordinate value of Full HD screen
MAX_X = 1920


class Node(ABC):
    def __init__(self, url):
        self.tag = None
        self.url = url
        # the default action to the target is click
        self.action = Action.NONE
        self.target = None
        self.label = None
        self.value = None
        self.xpath = None
        self.status = None
        self.rect = None
        self.metrics = None

    def __iter__(self):
        yield from {
            "tag": self.tag and self.tag,
            "label": self.label and self.label,
            "value": self.value and self.value,
            "target": self.target and self.target,
            "action": self.action and self.action.value,
            "xpath": self.xpath and self.xpath,
            "url": self.url and self.url,
            "status": self.status and self.status.value,
            "rect": self.rect and self.rect,
            "metrics": self.metrics and self.metrics.__dict__
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def to_json(self):
        return self.__str__()

    @staticmethod
    def from_json(json_data):
        url = util.safe_get_dict_item(json_data, 'url')

        node_obj = Node(url)
        node_obj.tag = util.safe_get_dict_item(json_data, 'tag')
        node_obj.label = util.safe_get_dict_item(json_data, 'label')
        node_obj.value = util.safe_get_dict_item(json_data, 'value')
        node_obj.target = util.safe_get_dict_item(json_data, 'target')
        node_obj.xpath = util.safe_get_dict_item(json_data, 'xpath')
        node_obj.rect = util.safe_get_dict_item(json_data, 'rect')

        status = util.safe_get_dict_item(json_data, 'status')
        if status:
            node_obj.status = NodeStatus(status)
        action = util.safe_get_dict_item(json_data, 'action')
        if action:
            node_obj.action = Action(action)
        else:
            if node_obj.tag:
                node_obj.action = Action.CLICK
            else:
                node_obj.action = Action.OPEN

        metrics_data = util.safe_get_dict_item(json_data, 'metrics')
        if metrics_data and metrics_data != 'null':
            node_obj.metrics = PageMetrics.from_json(metrics_data)

        return node_obj

    def get_key(self):
        if self.xpath:
            return self.url + " " + self.xpath
        else:
            return self.url

    def parse(self, element):
        # Todo : make element.is_enable() into js and add conditions
        # JS
        if type(element) is dict:
            self.tag = element["tag"]
            self.rect = element["rect"]

            # value means the inner text string displayed to the user
            self.label = element["label"]
            self.xpath = element["xpath"]
        # python
        else:
            self.tag = element.tag_name
            self.rect = element.rect
            # value means the inner text string displayed to the user
            self.label = self.find_label(element)

            self.xpath = xpath_util.get_relative_xpath(element)

        if self.tag == "a":
            if type(element) is dict:
                self.target = element["href"]
            else:
                self.target = element.get_attribute("href")
            # only if href has a value, the link is valid
            if not self.target:
                return False

        self.set_action(element)
        self.status = NodeStatus.Parsed

        # if there is no value, it is invisible so doesn't add to the graph
        # this should not happen for select_option
        if self.label:
            return True

        return False

    def set_action(self, element):
        def set_input_action():
            input_type = None

            if type(element) is dict:
                input_type = element["type"]
            else:
                input_type = element.get_attribute("type")

            if input_type and input_type in ["password", "number", "text"]:
                self.action = Action.TYPE

        if self.tag == "input":
            set_input_action()
        elif self.tag == "textarea":
            self.action = Action.TYPE
        else:
            if not self.tag:
                self.action = Action.OPEN
            else:
                self.action = Action.CLICK

    def is_within_view(self, max_width):
        """
        some elements are enabled and visible but outside the user view: e.g., elements within hamburger menu
        :return: True if visible
        """
        return self.rect and self.rect['height'] > 0 and self.rect['width'] > 0 and \
               0 <= self.rect['x'] < max_width and self.rect['y'] >= 0

    @handle_selenium_exceptions
    def act(self, driver):
        if not self.url:
            self.url = driver.current_url

        if self.action == Action.OPEN or self.action == Action.NONE:
            driver.get(self.url)
            selenium_util.handle_alert(driver)
            return True

        element = self.find_element(driver)
        if not element:
            return False

        # update the hidden element's rect
        if not self.is_within_view(MAX_X):
            # # update coordinates as some do not get correct values till they are found
            self.rect = element.rect

        # scroll to the element only if it is not displayed since scroll can trigger other events
        if not element.is_displayed():
            selenium_util.scroll_to_element(driver, element)

        logger.info("  mouse_move %s %s", self.label, self.xpath)
        selenium_util.mouse_move(driver, element)

        if self.action == Action.TYPE:
            element.send_keys(self.value)
        elif self.action == Action.CLICK:
            element.click()
            logger.info("  clicked %s", self.label)

        self.target = driver.current_url
        selenium_util.handle_alert(driver)

        return True

    def find_label(self, element):
        self.label = element.text

        if not self.label:
            self.label = element.get_attribute("id")
        if not self.label:
            self.label = element.get_attribute("name")
        if not self.label:
            self.label = element.get_attribute("value")
        if not self.label:
            self.label = element.get_attribute("class")
        if not self.label:
            self.label = element.get_attribute("title")

        if self.label:
            # remove unnecessary chars that might block encoding/decoding later
            self.label = self.label.strip().replace("\n", " ").replace("\"", "")

        return self.label

    def find_element(self, driver):
        logger.debug(" #finding %s %s", self.label, self.xpath)
        element = selenium_util.find_element_by_xpath_with_retries(driver, self.xpath)
        if element:
            return element
        else:
            self.status = NodeStatus.ElementNotFoundException
            logger.warning("can't find element (%s) in (%s)", self.label, self.url)

    def is_error(self):
        return not self.status and self.status not in {
            NodeStatus.Actionable,
            NodeStatus.Filtered,
            NodeStatus.Hidden,
            NodeStatus.Parsed
        }
