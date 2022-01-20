"""
Copyright (C) 2020 TestWorks Inc.
2020-02-25: 조규현(ghjo) created.
"""

from .i_command import ICommand

from selenium.webdriver.support.ui import Select

from src.util.selenium_util import get_element
from src.util.util import split_command
from src.util.logger import get_logger

logger = get_logger(__name__)


class SelectCommand(ICommand):
    """
    콤보박스 선택 명령입니다.
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

    def get_instance(self, web_driver, target, value, env, os_ver, browser, browser_version, test_option):
        return SelectCommand(web_driver, target, value, env, os_ver, browser, browser_version, test_option)
