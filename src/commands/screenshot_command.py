"""
Copyright (C) 2020 TestWorks Inc.
2020-03-25: 조연진 (yjcho@) created.
2020-04-01: 조연진 (yjcho@) 명령 수행 결과와 스크린샷 이미지 링크를 함께 반환하도록 수정
"""
import os
import settings
import datetime

from .command import Command

from src.util.util import connect_ftp, upload_image, close_ftp
from src.util.logger import get_logger

logger = get_logger(__name__)


class ScreenshotCommand(Command):
    """
    스크린샷 명령입니다.
    """
    def execute(self):
        """
        스크린샷 명령의 경우, 명령 수행 결과와 이미지 링크를 함께 리턴합니다.
        """
        logger.info("screenshot: %s", self.target)
        now = datetime.datetime.now()
        nowstr = str(now.replace(microsecond=0)).replace("-", "").replace(":", "").replace(" ", "_")
        detailed_info = "{0}_{1}_{2}_{3}_{4}".format(self.env, self.os_ver, self.browser, self.browser_version, settings.HOST_NAME)

        cur_frame = self.web_driver.find_element_by_id('currentFrameNumber')
        cur_frame = int(cur_frame.get_attribute("value"))
        file_name = "_frame_{}_{}.png".format(nowstr, cur_frame)

        # file_name = nowstr + "_" +  detailed_info + ".png"
        file_path = settings.FILE_PATH + file_name

        logger.info("Saving {}".format(file_path))
        try:
            self.web_driver.save_screenshot(file_path)
        except Exception as ex:
            logger.error("%s", ex)
            pf_result = False

        logger.info("Saved {}".format(file_path))
        # try:
        #     # FTP서버에 접속
        #     session = connect_ftp(settings.FILE_ADDRESS, settings.FILE_USERNAME, settings.FILE_PASSWORD)
        #
        #     # 전송할 파일 열기
        #     image_file = open(file_path, 'rb')
        #
        #     # FTP에 파일 전송
        #     upload_image(session, settings.FILE_UPLOAD_PATH + file_name, image_file)
        #     ftp_link = "ftp://" + settings.FILE_ADDRESS + "/" + settings.FILE_UPLOAD_PATH + file_name
        #
        #     # FTP세션 및 파일 닫기
        #     close_ftp(session, image_file)
        # except Exception as ex:
        #     logger.error("%s", ex)
        #     pf_result = False

        # # 로컬(.png) 파일 삭제
        # os.remove(file_path)

        pf_result = True

        return [pf_result, None]
