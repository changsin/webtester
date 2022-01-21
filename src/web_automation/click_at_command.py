"""
Copyright (C) 2022 TestWorks Inc.
2022-01-22: (changsin@) created.
"""

import ctypes
import time

from src.util.logger import get_logger
from .i_command import ICommand

logger = get_logger(__name__)


class ClickAtCommand(ICommand):
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
        x, y = self.value.split(",")
        x = int(x)
        y = int(y)
        logger.info("clickAt: {} {} {}".format(self.target, x, y))

        ctypes.windll.user32.SetCursorPos(x, y)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up

        time.sleep(2)

        return True
