"""
Copyright (C) 2022 TestWorks Inc.
2022-01-22: (changsin@) created.
"""

import ctypes
import time

from .i_command import ICommand
from selenium.webdriver.common.action_chains import ActionChains

from src.util.selenium_util import get_element, scroll_to_element
from src.util.logger import get_logger

logger = get_logger(__name__)


class SnapshotCommand(ICommand):
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
        script = """
            return {...window.cvat.data.get()};
            """
        collected = self.web_driver.execute_script(script)

        logger.info("class snapshot: {}".format(collected))

        return True
