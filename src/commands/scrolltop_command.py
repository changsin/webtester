"""
Copyright (C) 2020 TestWorks Inc.
2020-03-25: 조연진 (yjcho@) created.
"""

from .command import Command
from src.util.logger import get_logger

logger = get_logger(__name__)


class ScrollTopCommand(Command):
    def execute(self):
        logger.info("scrollTop: %s", self.target)

        try:
            self.web_driver.execute_script('window.scrollTo(%s, %s);' % (0, 0))
        except Exception as ex:
            logger.error(ex)
            return False

        return True
