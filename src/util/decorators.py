"""
Copyright (C) 2020 TestWorks Inc.

2020-03-05: changsin@ created
    a collection of python decorators

"""
import functools
# from timeit import time

from selenium.common import exceptions

from src.util.selenium_util import handle_alert
from .logger import get_logger

logger = get_logger(__name__)


def log_function_call(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        logger.info('->%s', func.__name__)
        val = func(*args, **kwargs)
        logger.info('<-%s', func.__name__)
        return val

    return wrapped_func


def calc_time(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        start_time = time.time()
        val = func(*args, **kwargs)
        end_time = time.time()
        logger.info('Function time: %s(%.2fs)',
                    func.__name__, end_time - start_time)
        return val

    return wrapped_func


def handle_selenium_exceptions(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        val = None

        try:
            val = func(*args, **kwargs)
        except exceptions.UnexpectedAlertPresentException as ex:
            if hasattr(kwargs[0], 'driver'):
                handle_alert(args[0].driver)
            else:
                logger.error('Unexpected alert present exception: %s(%s), alert text: %s', func.__name__, args[0], ex.alert_text)
        except exceptions.StaleElementReferenceException as ex:
            logger.warning('%s(%s) %s', func.__name__, args[0], ex)
            val = ex
        except exceptions.NoSuchElementException as ex:
            logger.warning('%s(%s) %s', func.__name__, args[0], ex)
            val = ex
        except exceptions.ElementNotInteractableException as ex:
            logger.warning('%s(%s) %s', func.__name__, args[0], ex)
            val = ex
        except exceptions.ElementClickInterceptedException as ex:
            logger.warning('%s(%s) %s', func.__name__, args[0], ex)
            val = ex
        except exceptions.TimeoutException as ex:
            logger.warning('%s(%s) %s', func.__name__, args[0], ex)
            val = ex
        except Exception as ex:
            logger.error('Unknown exception: %s(%s) %s', func.__name__, args[0], ex)
            val = ex

        return val

    return wrapped_func
