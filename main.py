import os
import sys
import json
import argparse
import platform
import multiprocessing
import settings

from src.executor.selenium_executor import SeleniumExecutor
from src.model.options import Options
from src.util import util
from src.util.logger import get_logger

logger = get_logger(__name__)

def crawl(start_url, options_file_path):
    options = Options.from_json(options_file_path)

    selenium_executor = SeleniumExecutor.create(settings.CHROME_DRIVER_PATH, options)

    crawler = Crawler(selenium_executor.driver, options, path)

    source_node = crawler.crawl(start_url, depth)
    logger.info("source_node is %s", source_node)

    selenium_executor.driver.get("https://aiworks.co.kr")

    selenium_executor.close()

    return graph_file_path


if __name__ == '__main__':

    multiprocessing.freeze_support()

    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='starting url')
    parser.add_argument('--options', help='path to options file')
    parser.add_argument('--depth', help='crawl depth')

    # Required folder name when analysis is started - ex) [URL]_001, [URL]_002, ...
    parser.add_argument('--folder', help='project folder name')
    
    args = parser.parse_args()

    # Analysis - *.json(graph)
    save_root = util.convert_path("{}/{}/{}/screenshot/".format(settings.FILE_PATH, 'projects', args.folder))
    graph_file_path = crawl(args.url, args.options)
