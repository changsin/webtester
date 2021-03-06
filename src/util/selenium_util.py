import time

from selenium.common import exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.util.util import logger


def scroll_to_element(driver, element):
    x = element.location['x']
    y = element.location['y']
    driver.execute_script('window.scrollTo(%s, %s);' % (x, y - 100))


def mouse_move(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element(element)
    try:
        actions.perform()

        time.sleep(0.5)

        return True
    except Exception as ex:
        logger.error("%s", ex)

    return False


def find_element_with_retries(driver, by, value):
    max_retries = 1
    retries = 0

    element = driver.find_element(by, value)
    if not element:
        return None

    while max_retries > retries:
        try:
            WebDriverWait(driver, 3)\
                .until(EC.element_to_be_clickable((by, value)))
            return element
        except exceptions.UnexpectedAlertPresentException:
            handle_alert(driver)
        except exceptions.StaleElementReferenceException as ex:
            logger.warning(ex)
            retries = retries + 1
            logger.warning(" *Retrying... %d", retries)
        except exceptions.TimeoutException:
            logger.warning("TimeoutException ")
            retries = retries + 1
            logger.warning("  *Retrying... %d", retries)
        except Exception as ex:
            logger.error("Exception occurred during element identification.")
            logger.error(ex)
            break


def find_elements_by_class_with_retries(driver, class_name):
    return find_element_with_retries(driver, By.CLASS_NAME, class_name)


def find_element_by_xpath_with_retries(driver, xpath):
    return find_element_with_retries(driver, By.XPATH, xpath)


def handle_alert(driver):
    try:
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        if alert:
            logger.warning(f"Alert present! Alert text: {alert.text}")
            alert.accept()
    except exceptions.NoAlertPresentException as ex:
        logger.debug(ex)
    except exceptions.TimeoutException as ex:
        logger.debug(ex)


def get_element(web_driver, path: str) -> WebElement:
        """
        WebElement??? ???????????? ??????. ???????????? None ??????
        path ??? ?????? ??? ?????? = ??? ???????????? [identifier]=[actual path] ??? ????????? ??????
        ?????? 4?????? ????????? ?????????
        id=[path]
        xpath=[path]
        linkText=[path]
        css=[path]
        """
        seperator_index = path.find("=")
        search_method = path[0:seperator_index]
        actual_path = path[seperator_index + 1:]
        element = None
        wait = WebDriverWait(web_driver, 60)

        try:
            if "id" == search_method:
                wait.until(EC.presence_of_element_located((By.ID, actual_path)))
                element = web_driver.find_element_by_id(actual_path)
            elif "xpath" == search_method:
                wait.until(EC.presence_of_element_located((By.XPATH, actual_path)))
                element = web_driver.find_element_by_xpath(actual_path)
            elif "linkText" == search_method:
                wait.until(EC.presence_of_element_located((By.LINK_TEXT, actual_path)))
                element = web_driver.find_element_by_link_text(actual_path)
            elif "name" == search_method:
                wait.until(EC.presence_of_element_located((By.NAME, actual_path)))
                element = web_driver.find_element_by_name(actual_path)
            elif "css" == search_method:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, actual_path)))
                element = web_driver.find_element_by_css_selector(actual_path)
        except exceptions.NoSuchElementException as ex:
            logger.error("%s", ex)
            return None

        return element


def scroll_to_element(web_driver, element):
        """
        element??? ?????? ???????????? ????????? ?????? ??????
        """
        x = element.location['x']
        y = element.location['y']
        web_driver.execute_script('window.scrollTo(%s, %s);' % (x, y - 100))


def wait(web_driver, wait_time):
        """
        wait_time : ???????????? ??????????????? ?????? ?????? ??? ?????? ???????????? ??????
        """
        web_driver.implicitly_wait(30)
        wait = WebDriverWait(web_driver, wait_time)
        wait.until(EC.presence_of_all_elements_located)


def wait_for_javascript_load(web_driver):
        """
        ????????????????????? ???????????? ?????? ???????????? ??????
        """
        result = None
        start_time = time.time()
        while "complete" != result:
            result = web_driver.execute_script('return document.readyState;')
            if time.time() - start_time > 120:
                print("time out - wait_for_javascript_load")
                return False

        return True


def wait_for_page_load(web_driver):
        """
        ????????????????????? ?????? ???????????? ????????? ????????? ??? ?????? ???????????? ??????
        """
        # ????????? javascript??? ??? ????????? ????????? ????????? ??? ?????? ????????? ?????? ??????
        try:
            wait(web_driver, 5)
            wait_for_javascript_load(web_driver)
            wait(web_driver, 5)
            wait_for_javascript_load(web_driver)
        except Exception as ex:
            logger.warning("%s", ex)


def get_scroll_height(web_driver):
        """
        ??? ???????????? ?????? ????????? ????????? ??????
        """
        try:
            scroll_height = web_driver.execute_script("return document.body.parentNode.scrollHeight")
        except Exception as ex:
            logger.error("%s", ex)
            return False

        return scroll_height


def get_viewport_height(web_driver):
        """
        ??? ???????????? viewport ????????? ????????? ??????
        """
        try:
            viewport_height = web_driver.execute_script("return window.innerHeight")
        except Exception as ex:
            logger.error("%s", ex)
            return False

        return viewport_height


def get_current_frame_number(web_driver):
    cur_frame = web_driver.find_element_by_id('currentFrameNumber')
    return int(cur_frame.get_attribute("value"))

