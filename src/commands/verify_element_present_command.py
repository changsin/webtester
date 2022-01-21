"""
Copyright (C) 2020 TestWorks Inc.
2020-04-28: 신용진 (yjshin@) created.
"""

from .command import Command
from src.util.selenium_util import get_element
from src.util.logger import get_logger

logger = get_logger(__name__)


class VerifyElementPresentCommand(Command):
    def execute(self):
        logger.info("verify element present: %s", self.target)
        try:
            element = get_element(self.web_driver, self.target)
        except:
            logger.error("Can't find element")
            return False

        if element == None:
            logger.error("Can't find element")
            return False
        
        return True
