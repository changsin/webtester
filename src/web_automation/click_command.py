"""
Copyright (C) 2020 TestWorks Inc.
2020-02-18: 조규현 (ghjo@) created.
2020-02-19: 조규현 (ghjo@) ie, edge의 불안정성으로 인해 click을 Javascript가 아닌 Selenium API 기반으로 변경
"""

from .i_command import ICommand

from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys

from src.util.selenium_util import get_element, scroll_to_element
from src.util.util import split_command
from src.util.logger import get_logger

logger = get_logger(__name__)


class ClickCommand(ICommand):
    """
    클릭 명령입니다.
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
        logger.info("click: %s", self.target)
        try:
            element = get_element(self.web_driver, self.target)
            scroll_to_element(self.web_driver, element)
        except Exception as ex:
            logger.error("%s", ex)
            return False

        """
        모바일에서 스와이프 기능이 없어 클릭 못하는 element는 자바스크립트로 클릭 함수를 호출하면 클릭 가능
        단, PC 버전에서 문제가 있기 때문에 따로 분리해서 작성함
        """
        if self.test_option == "PC":
            try:
                element.click()
            except exceptions.ElementClickInterceptedException as ex:
                logger.error("%s", ex)
                element.send_keys(Keys.ENTER)
            except Exception as ex:
                logger.error("%s", ex)
                return False

        else:
            try:
                if split_command(self.target)[0] == 'xpath':
                    script = r"var element = document.evaluate('%s', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; element.click();" % (
                        split_command(self.target)[1])
                    self.web_driver.execute_script(script)
                else:
                    element.click()
            except exceptions.ElementClickInterceptedException as ex:
                logger.error("%s", ex)
                element.send_keys(Keys.ENTER)
            except Exception as ex:
                logger.error("%s", ex)
                return False

        return True

    def get_instance(self, web_driver, target, value, env, os_ver, browser, browser_version, test_option):
        return ClickCommand(web_driver, target, value, env, os_ver, browser, browser_version, test_option)
