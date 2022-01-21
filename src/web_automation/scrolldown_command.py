"""
Copyright (C) 2020 TestWorks Inc.
2020-03-25: 조연진 (yjcho@) created.
"""

from .i_command import ICommand
from src.util.common_message import ScrollInfo
from src.util.logger import get_logger

logger = get_logger(__name__)


class ScrollDownCommand(ICommand):
    """
    스크롤 Down 명령입니다.
    """

    def __init__(self, web_driver, target, value, env, os_ver, browser, browser_version, test_option):
        self.web_driver = web_driver
        self.target = target
        self.value = value
        self.env = env
        self.os_ver = os_ver
        self.browser = browser
        self.browser_version = browser_version
        self.test_option = test_option

    def execute(self):
        logger.info("scrollDown: %s", self.target)
        # viewport_height = Util.get_viewport_height(self.web_driver)

        try:
            # 현재 위치를 기준(상대위치)으로 하여 지정한 크기(px)만큼 스크롤을 이동
            self.web_driver.execute_script('window.scrollBy(%s, %s);' % (0, ScrollInfo.SCROLL_HEIGHT.value))
        except Exception as ex:
            logger.error(ex)
            return False

        return True
