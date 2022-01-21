"""
Copyright (C) 2020 TestWorks Inc.
2020-04-27: 신용진 (yjshin@) created.
"""

from .command import Command
from src.util.selenium_util import get_element
from src.util.logger import get_logger

logger = get_logger(__name__)


class SendKeysCommand(Command):
    def execute(self):
        logger.info("send keys : %s", self.value)
        element = get_element(self.web_driver, self.target)
        if None != element:
            try:
                element.send_keys(self.value)
            except Exception as ex:
                logger.error("%s", ex)
                return False

        return True
