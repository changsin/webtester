"""
Copyright (C) 2020 TestWorks Inc.
2020-03-25: 조연진 (yjcho@) created.
"""

from .i_command import ICommand
from src.util.logger import get_logger

logger = get_logger(__name__)


class ScrollTopCommand(ICommand):
    """
    스크롤 Top 명령입니다.
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
        logger.info("scrollTop: %s", self.target)

        try:
            self.web_driver.execute_script('window.scrollTo(%s, %s);' % (0, 0))
        except Exception as ex:
            logger.error(ex)
            return False

        return True

    def get_instance(self, web_driver, target, value, env, os_ver, browser, browser_version, test_option):
        return ScrollTopCommand(web_driver, target, value, env, os_ver, browser, browser_version, test_option)
