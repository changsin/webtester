"""
Copyright (C) 2020 TestWorks Inc.

2020-03-05: changsin@ created as a POC

    1. Given a url and depths
    2. Open the url
    3. Create a Page#1 object
    4. Collect all actionable elements
    5. For each actionable element in the Page#1:
        5-1. Find action, target and value
        5-2. Click the target
        5-3. If the target is within the Page#1
        5-4.    Then create an edge from the current element to the target
        5-5. Else
        5-6.    Create a new element
        5-7.    Create an edge (current element) -> (new element)

"""
import json
import os
import time
from queue import Queue

# import networkx as nx
# from PIL import ImageFont, ImageDraw, Image

from src.executor.selenium_executor import SeleniumExecutor
from src.metrics.page_metrics import PageMetrics
from src.model.node.node import NodeStatus, Node

from src.executor.selenium_executor import SeleniumExecutor
from src.util.decorators import calc_time
from src.util.logger import get_logger

logger = get_logger(__name__)


class Crawler:
    def __init__(self, driver, options, path):
        self.driver = driver
        self.graph = nx.DiGraph()
        self.options = options
        self.parsed = set()
        self.se = SeleniumExecutor(driver)
        self.page_metrics = list()
        self.to_parse_q = Queue()
        self.path = path

    @calc_time
    def crawl(self, source_url, depth):
        logger.info("->crawl(%s) depth %d", source_url, depth)
        start_node = Node(source_url)
        gh.safe_add_node(self.graph, start_node)

        self.to_parse_q.put((start_node, depth))

        while not self.to_parse_q.empty():
            target_node, level = self.to_parse_q.get()
            self.to_parse_q.task_done()
            logger.info("  parse queue size: %d", self.to_parse_q.qsize())

            source_url = target_node.url
            source_node = gh.get_node(self.graph, source_url)
            if source_node:
                self.se.reset_url(source_node.url)

            self.graph, cur_node = self.se.do_action_set(self.graph, source_node, target_node,
                                                         self.options.pre_constraints, self.options.post_constraints)

            if target_node.is_error():
                logger.warning("<-crawl(%s) level %d", target_node, level)
                continue

            logger.info("cur_node.url: (%s) current_url: (%s)", cur_node.url, self.driver.current_url)
            assert cur_node.url == self.driver.current_url

            # if we visited this page before, return the cur_node
            if url_util.normalize_url(cur_node.url) in self.parsed:
                logger.info("<-crawl(%s) in (%s) level %d", cur_node.label, cur_node.url, level)

                assert gh.safe_has_node(self.graph, source_node)
                assert gh.safe_has_node(self.graph, cur_node)
                gh.safe_add_edge(self.graph, source_node, cur_node)
            else:
                to_crawl, page_metrics = self.parse_page()
                self.parsed.add(url_util.normalize_url(self.driver.current_url))

                # visit each element on the parsed page
                self.act_on_nodes(cur_node, to_crawl, page_metrics)

                for el in to_crawl:
                    if el.status == NodeStatus.Actionable and level > 0:
                        self.to_parse_q.put((el, level - 1))

        logger.info("<-crawl(%s) depth %d", source_url, depth)
        return start_node
