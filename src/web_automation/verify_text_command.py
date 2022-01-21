"""
Copyright (C) 2020 TestWorks Inc.
2020-02-21: 조규현 (ghjo@) created.
"""

from .i_command import ICommand

from src.util.selenium_util import get_element
from src.util.logger import get_logger

logger = get_logger(__name__)

class VerifyTextCommand(ICommand):
    """
    텍스트 검증 커맨드 입니다.
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
        logger.info("verify text : %s", self.value)
        try:
            element = get_element(self.web_driver, self.target)
            text = element.text
        except Exception as ex:
            logger.error("%s", ex)
            return False

        if text != self.value:
            return False
            
        return True
