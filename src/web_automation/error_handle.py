"""
Copyright (C) 2020 TestWorks Inc.
2020-03-06: 조규현 (ghjo@) created.
"""

from .e_error_code import ErrorCode

from src.util.logger import get_logger

logger = get_logger(__name__)


def error_handling(error_code):
    if error_code == ErrorCode.EDGE_IE_ONLY_SUPPORTED_PAGE:
        logger.error("Edge : Internet Explorer 에서만 지원되는 페이지 입니다.")
        return ErrorCode.EDGE_IE_ONLY_SUPPORTED_PAGE

    return True