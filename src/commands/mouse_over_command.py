"""
Copyright (C) 2020 TestWorks Inc.
2020-02-18: 조규현 (ghjo@) created.
"""

from .command import Command
from selenium.webdriver.common.action_chains import ActionChains

from src.util.selenium_util import get_element, scroll_to_element
from src.util.logger import get_logger

logger = get_logger(__name__)


class MouseOverCommand(Command):
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
