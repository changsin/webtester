"""
Copyright (C) 2020 TestWorks Inc.
2020-02-18: 조규현 (ghjo@) created.
"""
from src.util.logger import get_logger

logger = get_logger(__name__)


class ICommand:
    """
    ICommand 인터페이스입니다. 실행, 인스턴스생성 메서드를 가지고 있습니다.
    """

    def execute(self):
        raise NotImplementedError
