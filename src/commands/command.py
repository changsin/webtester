"""
Copyright (C) 2020 TestWorks Inc.
2020-02-18: 조규현 (ghjo@) created.
"""
from abc import ABC, abstractmethod
from src.util.logger import get_logger

logger = get_logger(__name__)


class Command(ABC):
    def __init__(self, web_driver, target, value, env, os_ver, browser, browser_version, test_option):
        self.web_driver = web_driver
        self.target = target
        self.value = value
        self.env = env
        self.os_ver = os_ver
        self.browser = browser
        self.browser_version = browser_version
        self.test_option = test_option

    @abstractmethod
    def execute(self):
        raise NotImplementedError
