"""
Copyright (C) 2020 TestWorks Inc.

2020-03-30: yjshin@ created as a POC

"""
from src.util import selenium_util
from src.util.logger import get_logger
from .node import Node, NodeStatus
# from .node import Type

logger = get_logger(__name__)


class NodeSelectOption(Node):
    def __init__(self, url):
        super(NodeSelectOption, self).__init__(url)
        # self.type = Type.SELECT_OPTION

    # handle select-option sequence: first find the select element, then find the option
    #   cannot find the option element directly
    def find_element(self, driver):
        select_index = self.xpath.rindex("/")
        select_xpath = self.xpath[:select_index]
        element = selenium_util.find_element_by_xpath_with_retries(driver, select_xpath)
        if element:
            logger.info("  Finding option element (%s)", self.xpath)
            return selenium_util.find_element_by_xpath_with_retries(driver, self.xpath)
        else:
            self.status = NodeStatus.ElementNotFoundException
            logger.warning("can't find select_option element (%s) in (%s)", self.label, self.url)
            return None
