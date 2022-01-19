import time

from selenium.common import exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
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
                .until(ec.element_to_be_clickable((by, value)))
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
        WebDriverWait(driver, 2).until(ec.alert_is_present())
        alert = driver.switch_to.alert
        if alert:
            logger.warning(f"Alert present! Alert text: {alert.text}")
            alert.accept()
    except exceptions.NoAlertPresentException as ex:
        logger.debug(ex)
    except exceptions.TimeoutException as ex:
        logger.debug(ex)
