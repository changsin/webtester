"""
Copyright (C) 2022 TestWorks Inc.
2022-01-22: (changsin@) created.
"""

import os
import ctypes
if os.name == "posix":
    import autopy
import time

from src.util.logger import get_logger
from .command import Command

logger = get_logger(__name__)


class XKeybdCommand(Command):
    def execute(self):
        # keystroke = int(self.value, 16)
        key = self.value

        if os.name == "posix":
            autopy.key.type_string(key)
        elif os.name == "nt":
            ctypes.windll.user32.keybd_event(key, 0, 0, 0)  # Down
            ctypes.windll.user32.keybd_event(key, 0, 0x0002, 0)  # Up
        else:
            logger.warning("OS is " + os.name)

        time.sleep(2)

        return True
