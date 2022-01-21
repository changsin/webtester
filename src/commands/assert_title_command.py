"""
Copyright (C) 2020 TestWorks Inc.
2020-04-28: 신용진 (yjshin@) created.
"""

from .command import Command

from src.util.logger import get_logger

logger = get_logger(__name__)


class AssertTitleCommand(Command):
    def execute(self):
        logger.info("assert title : %s", self.target)
        
        try:
            title_text = self.web_driver.title
        except Exception as ex:
            logger.error("%s", ex)
            return False
        
        if title_text != self.target:
            logger.error("Don't match each value in title")
            return False

        return True
