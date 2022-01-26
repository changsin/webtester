"""
Copyright (C) 2020 TestWorks Inc.
2020-02-18: 조규현 (ghjo@) created.
"""
import time

from .e_error_code import ErrorCode
from .command import Command

from src.util.logger import get_logger

logger = get_logger(__name__)


class OpenURLCommand(Command):
    """
    입력된 url로 이동하는 명령입니다.
    """
    def execute(self):
        logger.info("open %s", self.target)
        
        try:
            self.web_driver.get(self.target)
        except Exception as ex:
            logger.error("%s", ex)
            return False
        
        if 'Internet Explorer 필요' in self.web_driver.title and 'MicrosoftEdge' in self.web_driver.name:
            return ErrorCode.EDGE_IE_ONLY_SUPPORTED_PAGE # Internet Explorer 에서만 작동하는 url

        time.sleep(10)
        return True
