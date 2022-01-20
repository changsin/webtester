"""
Copyright (C) 2020 TestWorks Inc.
2020-02-18: 조규현 (ghjo@) created.
2020-02-21: 조규현 (ghjo@) 각 커맨드 마다 대기시간 5초 추가
2020-02-25: 조규현 (ghjo@) 각 커맨드 대기시간 2초로 변경, Edge Internet Explorer만 지원하는 예외처리 추가
2020-03-06: 조규현 (ghjo@) 에러 처리 함수 추가
2020-03-18: 조연진 (yjcho@) JSON 스트링 형태의 커맨드를 불러오는 함수 추가
2020-03-25: 조연진 (yjcho@) RPA 명령어 추가 - screenShot, scrollPageUp & Down, scrollTop & Bottom
2020-03-31: 조연진 (yjcho@) 커맨드 수행 함수 분리 (파일, 스트링)
"""

import json
import time

from src.util.logger import get_logger
from src.util.selenium_util import wait_for_page_load
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

logger = get_logger(__name__)


class CommandManager:
    """
    웹 테스트 자동화를 위한 커맨드 매니지먼트 클래스입니다.
    """

    def __init__(self, web_driver):
        self.web_driver = web_driver
        self.commands = []
        self.commands_queue = []
        self.commands_dict = {
            "open": OpenURLCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "type": TypeCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "mouseOver": MouseOverCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "click": ClickCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "clickAndWait": ClickCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "verifyTitle": VerifyTitleCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "verifyText": VerifyTextCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "verifyChecked": VerifyCheckedCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "verifyElementPresent": VerifyElementPresentCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "pause": PauseCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "selectWindow": SelectWindowCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "selectFrame": SelectFrameCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "select": SelectCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "scrollPageUp": ScrollUpCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "scrollPageTop": ScrollTopCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "scrollPageDown": ScrollDownCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "scrollPageBottom": ScrollBottomCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "screenShot": ScreenshotCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "sendKeys": SendKeysCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "refresh": RefreshCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "assertText": AssertTextCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "assertTitle": AssertTitleCommand(0, 0, 0, 0, 0, 0, 0, 0),     
            "assertChecked": AssertCheckedCommand(0, 0, 0, 0, 0, 0, 0, 0),     
            "assertElementPresent": AssertElementPresentCommand(0, 0, 0, 0, 0, 0, 0, 0),
            "assertAlert": AssertAlertCommand(0, 0, 0, 0, 0, 0, 0, 0)
        }  # 여기에 사용할 명령어와 객체를 삽입합니다.

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

            self.__enqueue_command_by_file(commands)
        except Exception as ex:
            logger.error("%s", ex)
            return False

        return True

    def load_command_from_str(self, json_str):
        """
        JSON 스트링 형태의 UI VISION 의 Commands 를 불러온 뒤,
        해당 커맨트 개제체를 만들어 커맨트큐에 삽입하는 함수입니다. 
        """
        try:
            data = json.loads(json_str)
            commands = data['Commands']
            self.__enqueue_command_by_str(commands)
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

            try:
                wait_for_page_load(self.web_driver)
                time.sleep(0.5)
            except Exception as ex:
                logger.error("%s", ex)
                return index+1

            if not result:
                return index+1

        time.sleep(2)
        logger.info('Command finish')
        return 0

    def execute_command_by_str(self):
        """
        커맨드큐에 있는 커맨드 개체들을 실행하는 함수입니다.
        UI VISION 의 Commands 를 JSON 스트링 형태로 불러와 일부 스크립트를 실행할 경우,
        명령 한 줄이 끝날 때마다 여유시간(초)을 지정하지 않습니다. 
        """

        for command in self.commands_queue:

            if type(command).__name__ != "AssertAlertCommand":
                try:
                    self.web_driver.switch_to.alert.accept()
                except Exception as ex:
                    logger.error("%s", ex)
                    cm_result = False

            execution_result = command.execute()

            if type(execution_result) == bool:
                """ 스크린샷 명령 이외의 경우, 명령 수행 결과만을 반환함 """
                pf_result = execution_result
                ftp_link = None
            else:
                """ 스크린샷 명령의 경우, 명령 수행 결과와 FTP 링크를 함께 반환함 """
                pf_result = execution_result[0]
                ftp_link = execution_result[1]

            if True != error_handling(pf_result):
                pf_result = False

            try:
                alert = self.web_driver.switch_to.alert
                if alert != None:
                    continue
            except:
                pass

            try:
                wait_for_page_load(self.web_driver)
                time.sleep(0.5)
            except Exception as ex:
                logger.error("%s", ex)
                cm_result = False

            cm_result = True

        logger.info('Command finish')

        """ 명령 수행 결과(Pass/Fail), 스크립트 수행 결과(True/False), FTP 링크를 리턴하도록 함 """

        return [pf_result, cm_result, ftp_link]

    def __enqueue_command_by_file(self, commands, test_option="PC"):
        """
        자바스크립트로 들어온 커맨드들을 커맨드 개체로 만들어 커맨드큐에 삽입하는 함수입니다.
        """
        for command in commands:
            # 커맨드 안의 Value를 변수로 저장합니다.
            current_command = command["Command"]
            current_target = command["Target"]
            current_value = command["Value"]

            # UI Vision 포맷의 파일을 불어올 때는 아래 값들을 고려하지 않기 때문에 None으로 처리합니다.
            current_env = None
            current_os_ver = None
            current_browser = None
            current_browser_version = None
            current_test_option = test_option

            if "" == current_command:
                break

            new_command = self.commands_dict[current_command].get_instance(
                self.web_driver, current_target, current_value, current_env, current_os_ver, current_browser,
                current_browser_version, current_test_option)

            self.commands_queue.append(new_command)

        return

    def __enqueue_command_by_str(self, commands):
        """
        자바스크립트로 들어온 커맨드들을 커맨드 개체로 만들어 커맨드큐에 삽입하는 함수입니다.
        """
        for command in commands:
            # 커맨드 안의 Value를 변수로 저장합니다.
            current_command = command["Command"]
            current_target = command["Target"]
            current_value = command["Value"]

            current_env = command["Env"]
            current_os_ver = command["OsVer"]
            current_browser = command["Browser"]
            current_browser_version = command["BrowserVersion"]

            current_test_option = command["TestOption"]

            if "" == current_command:
                break

            new_command = self.commands_dict[current_command].get_instance(
                self.web_driver, current_target, current_value, current_env, current_os_ver, current_browser,
                current_browser_version, current_test_option)

            self.commands_queue.append(new_command)

        return
