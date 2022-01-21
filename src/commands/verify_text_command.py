"""
Copyright (C) 2020 TestWorks Inc.
2020-02-21: 조규현 (ghjo@) created.
"""

from .command import Command

from src.util.selenium_util import get_element
from src.util.logger import get_logger

logger = get_logger(__name__)


class VerifyTextCommand(Command):
    def execute(self):
        logger.info("verify text : %s", self.value)
        try:
            element = get_element(self.web_driver, self.target)
            text = element.text
        except Exception as ex:
            logger.error("%s", ex)
            return False

        if text != self.value:
            return False
            
        return True
