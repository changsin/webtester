"""
Copyright (C) 2020 TestWorks Inc.
2020-02-25: 조규현(ghjo) created.
"""

from .command import Command

from selenium.webdriver.support.ui import Select

from src.util.selenium_util import get_element
from src.util.util import split_command
from src.util.logger import get_logger

logger = get_logger(__name__)


class SelectCommand(Command):
    def execute(self):
        logger.info("select : %s in  %s", self.value, self.target)
        element = get_element(self.web_driver, self.target)
        
        select_method = split_command(self.value)[0]
        value = split_command(self.value)[1]

        try:
            select = Select(element)
            if "label" == select_method:
                select.select_by_value(value)
            else:
                raise Exception("Invalid argument...")

        except Exception as ex:
            try:
                select.select_by_visible_text(value)
            except: 
                logger.error("%s", ex)
                return False

        return True
