import argparse
import multiprocessing
import os

import settings
from src.executor.selenium_executor import SeleniumExecutor
from options import Options
from src.util import util
from src.util.logger import get_logger
from src.commands.command_manager import CommandManager

logger = get_logger(__name__)


def run_script(driver, file_path):
    exec_result = None

    try:
        cm = CommandManager(driver)
        cm.load_command_from_file(file_path)
        exec_result = cm.execute_command_by_file()
    except Exception as ex:
        logger.info("%s", ex)

    return exec_result


def crawl(script_file_path, options_file_path):
    options = Options.from_json(options_file_path)

    selenium_executor = SeleniumExecutor.create(settings.CHROME_DRIVER_PATH, options)

    exec_result = run_script(selenium_executor.driver, script_file_path)
    selenium_executor.close()

    return exec_result


if __name__ == '__main__':

    multiprocessing.freeze_support()

    parser = argparse.ArgumentParser()
    parser.add_argument('--script_path', help='script path')
    parser.add_argument('--options', help='path to options file')

    args = parser.parse_args()

    graph_file_path = crawl(args.script_path, args.options)
