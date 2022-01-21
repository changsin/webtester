"""
Copyright (C) 2020 TestWorks Inc.
2020-02-18: 조규현 (ghjo@) created.
"""

from .command import Command

from src.util.selenium_util import get_element
from src.util.logger import get_logger

logger = get_logger(__name__)


class TypeCommand(Command):
    def execute(self):
        logger.info("type : %s", self.value)
        element = get_element(self.web_driver, self.target)
        if None != element:
            try:
                element.clear()
                element.send_keys(self.value)
            except Exception as ex:
                logger.error("%s", ex)
                return False

        return True
