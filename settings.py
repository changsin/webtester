import os
import sys
import json
import platform

from src.util import util


if getattr(sys, 'frozen', False):
    FILE_PATH = os.path.dirname(sys.executable)
    os.chdir(FILE_PATH)
else:
    FILE_PATH = os.path.abspath(os.path.dirname(__file__))


CLIENT_MACHINE_INFO_PATH = util.convert_path(FILE_PATH + "/settings/client_machine_info.json")


with open(CLIENT_MACHINE_INFO_PATH) as f:
    CONFIGURATION = json.loads(f.read())

TARGET_FILE = CONFIGURATION["Module"]
WEBDRIVER_INFO = CONFIGURATION["WebdriverInfo"]

TARGET_FILE_PATH = util.convert_path(FILE_PATH + "/" + TARGET_FILE)
CHROME_DRIVER_PATH = util.convert_path(FILE_PATH + '/bin/driver/' + WEBDRIVER_INFO[0]["WebdriverName"] + "/" + \
                     WEBDRIVER_INFO[0]["WebdriverVersion"] + '/' + WEBDRIVER_INFO[0]["API"] + "/" + \
                     WEBDRIVER_INFO[0]["FileName"])