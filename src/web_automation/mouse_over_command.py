"""
Copyright (C) 2020 TestWorks Inc.
2020-02-18: 조규현 (ghjo@) created.
"""

from .i_command import ICommand
from selenium.webdriver.common.action_chains import ActionChains

from src.util.selenium_util import get_element, scroll_to_element
from src.util.logger import get_logger

logger = get_logger(__name__)


class MouseOverCommand(ICommand):
    def __init__(self, web_driver, target, value, env, os_ver, browser, browser_version, test_option):
        self.web_driver = web_driver
        self.target = target
        self.value = value
        self.env = env
        self.os_ver = os_ver
        self.browser = browser
        self.browser_version = browser_version
        self.test_option = test_option

    def execute(self):
        logger.info("mouse over : %s", self.target)
        element = get_element(self.web_driver, self.target)
        if None != element:
            scroll_to_element(self.web_driver, element)
            actions = ActionChains(self.web_driver)
            actions.move_to_element(element)
            try:
                actions.perform()
            except Exception as ex:
                logger.error("%s", ex)
                return False
        
        return True

    def get_instance(self, web_driver, target, value, env, os_ver, browser, browser_version, test_option):
        return MouseOverCommand(web_driver, target, value, env, os_ver, browser, browser_version, test_option)
