"""
Copyright (C) 2020 TestWorks Inc.
2020-02-21: 조규현 (ghjo@) created.
"""

from .command import Command
from src.util.logger import get_logger

logger = get_logger(__name__)


class VerifyTitleCommand(Command):
    def execute(self):
        logger.info("verify title : %s", self.target)
        
        try:
            title_text = self.web_driver.title
        except Exception as ex:
            logger.error("%s", ex)
            return False
        
        if title_text != self.target:
            return False

        return True
