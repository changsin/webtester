"""
Copyright (C) 2020 TestWorks Inc.
2020-04-28: 신용진 (yjshin@) created.
"""

from .i_command import ICommand
from src.util.selenium_util import get_element
from src.util.logger import get_logger

logger = get_logger(__name__)

class AssertElementPresentCommand(ICommand):
    """
    엘리먼트 검증 커맨드 입니다.
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
        logger.info("assert element present: %s", self.target)
        try:
            element = get_element(self.web_driver, self.target)
        except:
            logger.error("Can't find element")
            return False
        
        return True
