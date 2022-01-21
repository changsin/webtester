"""
Copyright (C) 2020 TestWorks Inc.
2020-02-18: 조규현 (ghjo@) created.
"""

from .e_error_code import ErrorCode
from .i_command import ICommand

from src.util.logger import get_logger

logger = get_logger(__name__)


class OpenURLCommand(ICommand):
    """
    입력된 url로 이동하는 명령입니다.
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
        logger.info("open %s", self.target)
        
        try:
            self.web_driver.get(self.target)
        except Exception as ex:
            logger.error("%s", ex)
            return False
        
        if 'Internet Explorer 필요' in self.web_driver.title and 'MicrosoftEdge' in self.web_driver.name:
            return ErrorCode.EDGE_IE_ONLY_SUPPORTED_PAGE # Internet Explorer 에서만 작동하는 url

        return True
