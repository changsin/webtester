"""
Copyright (C) 2022 TestWorks Inc.
2022-01-22: (changsin@) created.
"""

import ctypes
import time
import os
import autopy

from src.util.logger import get_logger
from .command import Command

logger = get_logger(__name__)


class XKeybdCommand(Command):
    def execute(self):
        # keystroke = int(self.value, 16)
        key = self.value
        autopy.key.type_string(key)
        # if os.name == "Windows":
        #     ctypes.windll.user32.keybd_event(keystroke, 0, 0, 0)  # Down
        #     ctypes.windll.user32.keybd_event(keystroke, 0, 0x0002, 0)  # Up
        # else:
        #     logger.warning("OS is " + os.name)

        time.sleep(2)

        return True
