"""
Copyright (C) 2022 TestWorks Inc.
"""

import json
import random
import time

from src.util.logger import get_logger
from src.util.selenium_util import wait_for_page_load
from src.util.util import safe_get_dict_item
from .assert_alert_command import AssertAlertCommand
from .assert_checked_command import AssertCheckedCommand
from .assert_element_present_command import AssertElementPresentCommand
from .assert_text_command import AssertTextCommand
from .assert_title_command import AssertTitleCommand
from .click_command import ClickCommand
from .error_handle import error_handling
from .mouse_over_command import MouseOverCommand
from .open_url_command import OpenURLCommand
from .pause_command import PauseCommand
from .refresh_command import RefreshCommand
from .screenshot_command import ScreenshotCommand
from .scrollbottom_command import ScrollBottomCommand
from .scrolldown_command import ScrollDownCommand
from .scrolltop_command import ScrollTopCommand
from .scrollup_command import ScrollUpCommand
from .select_command import SelectCommand
from .select_frame_command import SelectFrameCommand
from .select_window_command import SelectWindowCommand
from .send_keys_command import SendKeysCommand
from .type_command import TypeCommand
from .verify_checked_command import VerifyCheckedCommand
from .verify_element_present_command import VerifyElementPresentCommand
from .verify_text_command import VerifyTextCommand
from .verify_title_command import VerifyTitleCommand
from .x_click_at_command import XClickAtCommand
from .x_keybd_command import XKeybdCommand
from .x_snapshot_command import XSnapshotCommand

logger = get_logger(__name__)

BEGIN_LOOP = "BeginLoop"
END_LOOP = "EndLoop"
RANDOM = "{RANDOM}"


class CommandManager:
    """
    """

    def __init__(self, web_driver):
        self.web_driver = web_driver
        self.commands = []
        self.commands_queue = []
        self.commands_dict = {
            "open": OpenURLCommand,
            "type": TypeCommand,
            "mouseOver": MouseOverCommand,
            "click": ClickCommand,
            "clickAndWait": ClickCommand,
            "verifyTitle": VerifyTitleCommand,
            "verifyText": VerifyTextCommand,
            "verifyChecked": VerifyCheckedCommand,
            "verifyElementPresent": VerifyElementPresentCommand,
            "pause": PauseCommand,
            "selectWindow": SelectWindowCommand,
            "selectFrame": SelectFrameCommand,
            "select": SelectCommand,
            "scrollPageUp": ScrollUpCommand,
            "scrollPageTop": ScrollTopCommand,
            "scrollPageDown": ScrollDownCommand,
            "scrollPageBottom": ScrollBottomCommand,
            "screenShot": ScreenshotCommand,
            "sendKeys": SendKeysCommand,
            "refresh": RefreshCommand,
            "assertText": AssertTextCommand,
            "assertTitle": AssertTitleCommand,     
            "assertChecked": AssertCheckedCommand,     
            "assertElementPresent": AssertElementPresentCommand,
            "assertAlert": AssertAlertCommand,
            "x_clickAt": XClickAtCommand,
            "x_keybd": XKeybdCommand,
            "x_snapshot": XSnapshotCommand,
        }

    def load_command_from_file(self, path) -> bool:
        """
        자바스크립트로 저장된 UI VISION 의 Commands 파일을 불러온 뒤,
        해당 커맨드 개체를 만들어 커맨드큐에 삽입하는 함수입니다.
        """
        try:
            f = open(path, "r", encoding="utf-8")
            data = json.load(f)
            f.close()
            commands = data['Commands']

            self.__enqueue_commands(commands)
        except Exception as ex:
            logger.error("%s", ex)
            return False

        return True

    def execute_command_by_file(self):
        """
        커맨드큐에 있는 커맨드 개체들을 실행하는 함수입니다.
        UI VISION 의 Commands 파일을 불러와 전체 스크립트를 실행할 경우, 
        명령 한 줄을 정상적으로 완료하기 위한 여유시간(초)를 추가해야 합니다.
        return value : 오류가 발생한 commnad의 index + 1, 정상 수행 = 0
        """
        # for command in self.commands_queue:
        for index in range(len(self.commands_queue)):
            command = self.commands_queue[index]

            if type(command).__name__ != "AssertAlertCommand":
                try:
                    self.web_driver.switch_to.alert.accept()
                except:
                    pass

            result = command.execute()
            
            if True != error_handling(result):
                return index+1

            try:
                alert = self.web_driver.switch_to.alert
                if alert != None:
                    continue
            except:
                pass
            if not type(command).__name__.startswith("X"):
                try:
                    wait_for_page_load(self.web_driver)
                    time.sleep(0.5)
                except Exception as ex:
                    logger.error("%s", ex)
                    return index+1
            else:
                logger.info("=== not waiting {}".format(type(command).__name__))

            if not result:
                return index+1

        time.sleep(1)
        logger.info('Command finish')
        return 0

    def __enqueue_commands(self, commands, test_option="PC"):
        loop_began = False
        loop_queue = []
        for command in commands:
            current_command = command["Command"]
            current_target = command["Target"]
            current_value = command["Value"]

            env = safe_get_dict_item(command, "Env")
            os_ver = safe_get_dict_item(command, "OsVer")
            browser = safe_get_dict_item(command, "Browser")
            browser_version = safe_get_dict_item(command, "BrowserVersion")

            current_test_option = safe_get_dict_item(command, "TestOption")

            if "" == current_command:
                break

            if BEGIN_LOOP == current_command:
                loop_began = True
                continue

            if loop_began:
                if END_LOOP != current_command:
                    new_command = self.commands_dict[current_command](
                        self.web_driver, current_target, current_value,
                        env, os_ver, browser, browser_version, current_test_option)

                    loop_queue.append(new_command)
                    continue
                else:
                    loop_began = False
                    times = int(current_value)

                    for id in range(times):
                        if current_target == RANDOM:
                            id = random.randint(0, len(loop_queue) - 1)
                        self.commands_queue.append(loop_queue[id])
                continue

            new_command = self.commands_dict[current_command](
                self.web_driver, current_target, current_value,
                env, os_ver, browser, browser_version, current_test_option)

            self.commands_queue.append(new_command)
