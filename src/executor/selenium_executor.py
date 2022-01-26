"""
Copyright (C) 2020 TestWorks Inc.

2020-03-17: changsin@ created as a POC

"""
import time

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options as cOptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.util import util
from src.util.decorators import log_function_call
from src.util.logger import get_logger
from src.util.selenium_util import handle_alert

logger = get_logger(__name__)


class SeleniumExecutor:
    def __init__(self, driver):
        self.driver = driver
        self.is_mobile = False

    def close(self):
        if self.driver:
            self.driver.close()

    @staticmethod
    def create(chrome_driver_path, watts_options):
        coptions = cOptions()

        # run headless
        if watts_options and watts_options.browser_options:
            is_headless = util.safe_get_dict_item(watts_options.browser_options, "headless")
            if is_headless and is_headless == "True":
                coptions.add_argument("--headless")

            width = util.safe_get_dict_item(watts_options.browser_options, "width")
            height = util.safe_get_dict_item(watts_options.browser_options, "height")
            pixel_ratio = util.safe_get_dict_item(watts_options.browser_options, "pixel_ratio")
            if width and height and pixel_ratio:
                # ref : https://chromedriver.chromium.org/mobile-emulation
                mobile_emulation = {"deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 1.0},
                                    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
                mobile_emulation["deviceMetrics"]["width"] = width
                mobile_emulation["deviceMetrics"]["height"] = height
                mobile_emulation["deviceMetrics"]["pixelRatio"] = pixel_ratio
                coptions.add_experimental_option("mobileEmulation", mobile_emulation)
                logger.info("Browser Option : %s(%s), %s(%s), %s(%s)",
                            width, type(width), height, type(height), pixel_ratio, type(pixel_ratio))

        # # load without images
        # prefs = {'profile.managed_default_content_settings.images': 2}
        # coptions.add_experimental_option("prefs", prefs)

        coptions.add_argument('--start-maximized')
        coptions.add_argument('--disable-infobars')
        # coptions.add_argument('--disable-popup-blocking')
        # coptions.add_argument('--window-size=1920x1080')
        # coptions.add_argument('--lang=ko-kr')
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=coptions)
        driver.maximize_window()
        # driver.implicitly_wait(5)

        return SeleniumExecutor(driver)

    def execute_scripts(self, scripts):
        for script in scripts:
            self.driver.execute_script(script)

    def go_back(self):
        logger.info("go_back in page history")
        self.driver.execute_script("window.history.go(-1)")

    def reset_url(self, url):
        # reset it every time since there could be a popup blocking interaction with the elements underneath
        logger.info("  *resetting the url from (%s) to (%s)", self.driver.current_url, url)
        try:
            self.driver.get(url)
        except exceptions.UnexpectedAlertPresentException as ex:
            logger.warning(f"Unexpected alert present. alert text: {ex.alert_text}")
            handle_alert(self.driver)
            self.driver.get(url)
        time.sleep(0.5)

    def run_constraints(self, graph, source_node, target_node, constraints):
        """
        simply runs constraints if there are any
        There can be two types of constraints:
            1. against the web page (url)
            2. against a specific element

        It runs the constraints for #1 first, then #2 second
        """
        cur_node = source_node

        if source_node:
            # run page-wide constraints first
            node_constraints = util.safe_get_dict_item(constraints, source_node.url)
            if node_constraints:
                graph, cur_node = self.run_node_series(graph, cur_node, node_constraints)

            # run per element constraints next
            if source_node.get_key() != source_node.url:
                node_constraints = util.safe_get_dict_item(constraints, source_node.get_key())
                if node_constraints:
                    graph, cur_node = self.run_node_series(graph, cur_node, node_constraints)

        # check if there are any element-wise constraints
        if target_node:
            node_constraints = util.safe_get_dict_item(constraints, target_node.get_key())
            if node_constraints:
                graph, cur_node = self.run_node_series(graph, cur_node, node_constraints)

        return graph, cur_node


    def wait_for_page_load(self, old_page, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(ec.staleness_of(old_page))
        except exceptions.TimeoutException:
            logger.debug("TimeoutException for page refresh")
        except exceptions.UnexpectedAlertPresentException as ex:
            logger.debug(f"Unexpected alert presents, alert text: {ex.alert_text}")
        except Exception as ex:
            logger.error("Exception occurred during element identification.")
            logger.error(ex)
