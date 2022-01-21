"""
Copyright (C) 2020 TestWorks Inc.
2020-02-23: 임정현(jhim) created.
"""

import time

from .command import Command

from src.util.logger import get_logger

logger = get_logger(__name__)


class PauseCommand(Command):
    """
    pause 명령입니다.
    target : sleep 시간(mili second)
    """
    def execute(self):
        logger.info("execute : pause : %s ms", self.target)
        time.sleep(int(self.target) / 1000)
        return True
