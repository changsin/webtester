"""
Copyright (C) 2020 TestWorks Inc.
2020-02-23: 임정현(jhim) created.
"""

import time

from .i_command import ICommand

from src.util.logger import get_logger

logger = get_logger(__name__)


class SelectWindowCommand(ICommand):
    """
    selectWindow 명령입니다.
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
        logger.info("execute : selectWindow : %s", self.target)
        params = str(self.target).lower().split("=")

        if len(params) != 2:
            raise Exception("Invalid argument...")

        target_window = params[0]

        if target_window == "tab":
            target_index = int(params[1])
            self.__activate_tab(target_index)
        elif target_window == "title":
            target_title = params[1]
            self.__activate_title(target_title)
        else:
            raise Exception("Invalid argument...")

        return True

    def __activate_tab(self, index):
        if len(self.web_driver.window_handles) > index:
            self.web_driver.switch_to.window(self.web_driver.window_handles[index])
        else:
            raise Exception("Invalid argument(index)...")
    
    def __activate_title(self, title):
        if type(title) == str:
            for i in range(len(self.web_driver.window_handles)):
                self.web_driver.switch_to.window(self.web_driver.window_handles[i])
                if self.web_driver.title == title:
                    break   
        else:
            raise Exception("Invaild argument(title)...")

    def get_instance(self, web_driver, target, value, env, os_ver, browser, browser_version, test_option):
        return SelectWindowCommand(web_driver, target, value, env, os_ver, browser, browser_version, test_option)
