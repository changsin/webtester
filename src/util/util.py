"""
Copyright (C) 2020 TestWorks Inc.

2020-03-05: changsin@ created as a POC

"""
import json
import sys
import ftplib
import subprocess
import string

from .logger import get_logger

logger = get_logger(__name__)


# which platform am I running from?
def get_platform():
    platforms = {
        'linux1': 'linux',
        'linux2': 'linux',
        'darwin': 'mac64',
        'win32': 'win32'
    }

    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


# return the correct font for displaying Korean & other chars
def get_font():
    if get_platform() == 'win32':
        return "Malgun Gothic"
    else:
        return "AppleGothic"


# return the correct font file for displaying Korean & other chars
def get_font_file():
    if get_platform() == 'win32':
        return "malgunbd.ttf"
    else:
        return "AppleGothic.ttf"


# check path and convert to win32 type if necessary
def convert_path(path):
    if get_platform() == 'win32':
        return path.replace('/', '\\')
    else:
        return path


def load_json_file(path):
    try:
        f = open(path, "r", encoding="utf-8")
        data = json.load(f)
        f.close()
        return data

    except Exception as ex:
        logger.error(ex)


def safe_get_dict_item(data_dict, key):
    """
    check if the key exists in the dict before trying to access it
    :param data_dict:
    :param key:
    :return: item if found, Non otherwise
    """
    value = data_dict.get(key)
    if value is not None:
        obj = data_dict[key]
        if obj == 'None':
            return None
        else:
            return obj
    else:
        return None


def to_file(file_name, data):
    with open(file_name,  'w', encoding="utf-8") as json_file:
        json_file.write(data)


def execute_command(command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    except Exception as ex:
        logger.error(ex)


def check_output(command):
    try:
        output = subprocess.check_output(command)
        output = output.decode("utf-8")
        return output

    except Exception as ex:
        logger.error(ex)


def get_valid_file_name(target_string):
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    return target_string.translate(remove_punctuation_map)


def connect_ftp(file_server, username, password):
        """
        FTP에 연결하는 함수
        """
        # FTP 서버에 접속
        try:
            session = ftplib.FTP(file_server, username, password)
        except Exception as ex:
            logger.error("%s", ex)

        return session


def upload_image(session, upload_path, upload_file):
    """
    FTP에 스크린샷 이미지를 업로드하는 함수
    """
    try:
        session.storbinary('STOR ' + upload_path, upload_file)
    except Exception as ex:
        logger.error("%s", ex)


def close_ftp(session, upload_file):
    """
    FTP 세션 및 파일을 닫는 함수
    """
    try:
        session.quit()
        upload_file.close()
    except Exception as ex:
        logger.error("%s", ex)


def split_command(command):
        """
        = 로 구분되어있는 커맨드를 헤더와 바디로 나누어서 배열에 넣어 반환해 주는 함수
        """
        result = []
        seperator_index = command.find("=")
        result.append(command[0:seperator_index])
        result.append(command[seperator_index + 1:])

        return result
