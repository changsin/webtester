"""
Copyright (C) 2020 TestWorks Inc.
2020-02-25: 조규현(ghjo) created.
"""

from .i_command import ICommand
from src.util.selenium_util import get_element
from src.util.logger import get_logger

logger = get_logger(__name__)


class SelectFrameCommand(ICommand):
    """
    Frame switch 명령입니다.
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
        logger.info("switch frame : %s", self.target)
        element = get_element(self.web_driver, self.target)
        
        try:
            self.web_driver.switch_to.frame(element)
        except Exception as ex:
            logger.error("%s", ex)
            return False

        return True
