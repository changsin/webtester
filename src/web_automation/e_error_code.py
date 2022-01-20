"""
Copyright (C) 2020 TestWorks Inc.
2020-02-25: 조규현 (ghjo@) created.
"""
from enum import Enum

from src.util.logger import get_logger

logger = get_logger(__name__)


class ErrorCode(Enum):
    EDGE_IE_ONLY_SUPPORTED_PAGE = -3001