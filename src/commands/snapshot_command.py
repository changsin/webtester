"""
Copyright (C) 2022 TestWorks Inc.
2022-01-22: (changsin@) created.
"""

import ctypes
import time

from .command import Command
from selenium.webdriver.common.action_chains import ActionChains

from src.util.selenium_util import get_element, scroll_to_element
from src.util.logger import get_logger

logger = get_logger(__name__)


class SnapshotCommand(Command):
    def execute(self):
        script = """
            return {...window.cvat.data.get()};
            """
        collected = self.web_driver.execute_script(script)

        logger.info("class snapshot: {}".format(collected))

        return True
