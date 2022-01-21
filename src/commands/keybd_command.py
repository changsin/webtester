"""
Copyright (C) 2022 TestWorks Inc.
2022-01-22: (changsin@) created.
"""

import ctypes
import time

from src.util.logger import get_logger
from .command import Command

logger = get_logger(__name__)


class ClickAtCommand(Command):
    def execute(self):
        x, y = self.value.split(",")
        x = int(x)
        y = int(y)
        logger.info("clickAt: {} {} {}".format(self.target, x, y))

        ctypes.windll.user32.keybd_event(0x73, 0, 0, 0)  # F4 Down
        ctypes.windll.user32.keybd_event(0x73, 0, 0x0002, 0)  # F4 Up

        time.sleep(2)

        return True
