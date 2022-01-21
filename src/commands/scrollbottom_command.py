"""
Copyright (C) 2020 TestWorks Inc.
2020-03-25: 조연진 (yjcho@) created.
"""

from .command import Command

from src.util.selenium_util import get_scroll_height
from src.util.logger import get_logger

logger = get_logger(__name__)


class ScrollBottomCommand(Command):
    """
    스크롤 Bottom 명령입니다.
    """
    def execute(self):
        logger.info("scrollBottom: %s", self.target)
        scroll_height = get_scroll_height(self.web_driver)

        try:
            self.web_driver.execute_script('window.scrollTo(%s, %s);' % (0, scroll_height))
        except Exception as ex:
            logger.error(ex)
            return False

        return True
