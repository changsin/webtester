"""
Copyright (C) 2020 TestWorks Inc.
2020-03-25: 조연진 (yjcho@) created.
"""

from .command import Command
from src.util.selenium_util import get_viewport_height
from src.util.logger import get_logger

logger = get_logger(__name__)


class ScrollUpCommand(Command):
    def execute(self):
        logger.info("scrollUp: %s", self.target)
        viewport_height = get_viewport_height(self.web_driver)

        try:
            # 현재 위치를 기준(상대위치)으로 하여 지정한 크기(px)만큼 스크롤을 이동
            self.web_driver.execute_script('window.scrollBy(%s, %s);' % (0, -viewport_height))
        except Exception as ex:
            logger.error(ex)
            return False

        return True
