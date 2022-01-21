"""
Copyright (C) 2020 TestWorks Inc.
2020-04-27: 신용진 (yjshin@) created.
"""

from .command import Command

from src.util.logger import get_logger

logger = get_logger(__name__)


class RefreshCommand(Command):
    """
    텍스트 입력 명령입니다.
    """
    def execute(self):
        logger.info("refresh")
        try:
            self.web_driver.refresh()
        except Exception as ex:
            logger.error("%s", ex)
            return False
            
        return True
