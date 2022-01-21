"""
Copyright (C) 2020 TestWorks Inc.
2020-04-27: 신용진 (yjshin@) created.
"""

from .i_command import ICommand
from src.util.selenium_util import get_element
from src.util.logger import get_logger

logger = get_logger(__name__)


class SendKeysCommand(ICommand):
    """
    텍스트 입력 명령입니다.
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
        logger.info("send keys : %s", self.value)
        element = get_element(self.web_driver, self.target)
        if None != element:
            try:
                element.send_keys(self.value)
            except Exception as ex:
                logger.error("%s", ex)
                return False

        return True
