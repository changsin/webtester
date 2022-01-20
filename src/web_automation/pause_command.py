"""
Copyright (C) 2020 TestWorks Inc.
2020-02-23: 임정현(jhim) created.
"""

import time

from .i_command import ICommand

from src.util.logger import get_logger

logger = get_logger(__name__)


class PauseCommand(ICommand):
    """
    pause 명령입니다.
    target : sleep 시간(mili second)
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
        logger.info("execute : pause : %s ms", self.target)
        time.sleep(int(self.target) / 1000)
        return True

    def get_instance(self, web_driver, target, value, env, os_ver, browser, browser_version, test_option):
        return PauseCommand(web_driver, target, value, env, os_ver, browser, browser_version, test_option)
