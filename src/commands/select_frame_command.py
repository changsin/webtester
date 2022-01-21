"""
Copyright (C) 2020 TestWorks Inc.
2020-02-25: 조규현(ghjo) created.
"""

from .command import Command
from src.util.selenium_util import get_element
from src.util.logger import get_logger

logger = get_logger(__name__)


class SelectFrameCommand(Command):
    def execute(self):
        logger.info("switch frame : %s", self.target)
        element = get_element(self.web_driver, self.target)
        
        try:
            self.web_driver.switch_to.frame(element)
        except Exception as ex:
            logger.error("%s", ex)
            return False

        return True
