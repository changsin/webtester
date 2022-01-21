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

        ctypes.windll.user32.SetCursorPos(x, y)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up

        time.sleep(2)

        return True
