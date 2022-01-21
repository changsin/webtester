"""
Copyright (C) 2020 TestWorks Inc.
2020-03-25: 조연진 (yjcho@) created.
"""

from .i_command import ICommand

from src.util.selenium_util import get_scroll_height
from src.util.logger import get_logger

logger = get_logger(__name__)


class ScrollBottomCommand(ICommand):
    """
    스크롤 Bottom 명령입니다.
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
        logger.info("scrollBottom: %s", self.target)
        scroll_height = get_scroll_height(self.web_driver)

        try:
            self.web_driver.execute_script('window.scrollTo(%s, %s);' % (0, scroll_height))
        except Exception as ex:
            logger.error(ex)
            return False

        return True
