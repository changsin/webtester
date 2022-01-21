"""
Copyright (C) 2020 TestWorks Inc.
2020-04-27: 신용진 (yjshin@) created.
"""

from .command import Command

from src.util.logger import get_logger

logger = get_logger(__name__)


class AssertAlertCommand(Command):
    def execute(self):
        try:
            alert = self.web_driver.switch_to.alert
            logger.info("assert Alert : %s", alert.text)
        except Exception as ex:
            logger.error("%s", ex)
            return False

        if self.target != alert.text:
            logger.error("isn't match text in alert message")
            return False
        
        alert.accept()
        return True
