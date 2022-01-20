"""
Copyright (C) 2020 TestWorks Inc.
2020-04-10: 조연진 (yjcho@) created.
"""
from enum import Enum

from src.util.logger import get_logger

logger = get_logger(__name__)


class ClientInfo(Enum):
    PROGRAM_NAME = "TesterBench RPA Client"
    
class TestOption(Enum):
    PC = "PC"
    MOBILE = "MOBILE"

class SocketDataType(Enum):
    DEVICE_INFO = "DEVICE_INFO"
    RPA_COMMAND = "RPA_COMMAND"
    TEST_END = "TEST_END"

class Command(Enum):
    OPEN = "open"
    TYPE = "type"
    MOUSE_OVER = "mouseOver"
    CLICK = "click"
    CLICK_AND_WAIT = "clickAndWait"
    VERIFY_TITLE =  "verifyTitle"
    VERIFY_TEXT = "verifyText"
    PAUSE = "pause"
    SELECT_WINDOW = "selectWindow"
    SELECT_FRAME = "selectFrame"
    SELECT = "select"
    SCROLL_PAGE_UP = "scrollPageUp"
    SCROLL_PAGE_TOP = "scrollPageTop"
    SCROLL_PAGE_DOWN = "scrollPageDown"
    SCROLL_PAGE_BOTTOM = "scrollPageBottom"
    SCREENSHOT = "screenShot"

class ProcessType(Enum):
    CHROME = "chrome"
    INTERNET_EXPLORER = "iexplore"
    EDGE = "MicrosoftEDGE"
    FIREFOX = "firefox"
    CHROME_DRIVER = "chromedriver"
    IE_DRIVER = "IEDriverServer"
    EDGE_DRIVER = "MicrosoftWebDriver"
    FIREFOX_DRIVER = "geckodriver"
    NODE = "node"
    ADB = "adb"

class ScrollInfo(Enum):
    SCROLL_HEIGHT = 400

class AppiumServerValue(Enum):
    CONNECTION_TRY_COUNT = 3
    RETRY_WAIT_TIME = 10