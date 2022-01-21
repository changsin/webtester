"""
Copyright (C) 2020 TestWorks Inc.
2020-03-25: 조연진 (yjcho@) created.
2020-04-01: 조연진 (yjcho@) 명령 수행 결과와 스크린샷 이미지 링크를 함께 반환하도록 수정
"""
import os
import settings
import datetime

from .i_command import ICommand

from src.util.util import connect_ftp, upload_image, close_ftp
from src.util.logger import get_logger

logger = get_logger(__name__)


class ScreenshotCommand(ICommand):
    """
    스크린샷 명령입니다.
    """

    def __init__(self, web_driver, target, value, env, os_ver, browser, browser_version, test_option):
        self.web_driver = web_driver
        self.target = target
        self.value = value
        self.env = env
        self.os_ver = os_ver
        self.browser = browser
        self.browser_version = browser_version
        self.test_option = test_option

    def execute(self):
        """
        스크린샷 명령의 경우, 명령 수행 결과와 이미지 링크를 함께 리턴합니다.
        """
        logger.info("screenshot: %s", self.target)
        now = datetime.datetime.now()
        nowstr = str(now.replace(microsecond=0)).replace("-","").replace(":","").replace(" ", "_")
        detailed_info = "{0}_{1}_{2}_{3}_{4}".format(self.env, self.os_ver, self.browser, self.browser_version, settings.HOST_NAME)

        file_name = nowstr + "_" +  detailed_info + ".png"
        file_path = settings.FILE_PATH + file_name

        try:
            self.web_driver.save_screenshot(file_path)
        except Exception as ex:
            logger.error("%s", ex)
            pf_result = False

        try:
            # FTP서버에 접속
            session = connect_ftp(settings.FILE_ADDRESS, settings.FILE_USERNAME, settings.FILE_PASSWORD)

            # 전송할 파일 열기
            image_file = open(file_path, 'rb')

            # FTP에 파일 전송
            upload_image(session, settings.FILE_UPLOAD_PATH + file_name, image_file)
            ftp_link = "ftp://" + settings.FILE_ADDRESS + "/" + settings.FILE_UPLOAD_PATH + file_name

            # FTP세션 및 파일 닫기
            close_ftp(session, image_file)
        except Exception as ex:
            logger.error("%s", ex)
            pf_result = False

        # 로컬(.png) 파일 삭제
        os.remove(file_path)

        pf_result = True

        return [pf_result, ftp_link]
