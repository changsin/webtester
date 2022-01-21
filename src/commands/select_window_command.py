"""
Copyright (C) 2020 TestWorks Inc.
2020-02-23: 임정현(jhim) created.
"""

from src.util.logger import get_logger
from .command import Command

logger = get_logger(__name__)


class SelectWindowCommand(Command):
    def execute(self):
        logger.info("execute : selectWindow : %s", self.target)
        params = str(self.target).lower().split("=")

        if len(params) != 2:
            raise Exception("Invalid argument...")

        target_window = params[0]

        if target_window == "tab":
            target_index = int(params[1])
            self.__activate_tab(target_index)
        elif target_window == "title":
            target_title = params[1]
            self.__activate_title(target_title)
        else:
            raise Exception("Invalid argument...")

        return True

    def __activate_tab(self, index):
        if len(self.web_driver.window_handles) > index:
            self.web_driver.switch_to.window(self.web_driver.window_handles[index])
        else:
            raise Exception("Invalid argument(index)...")
    
    def __activate_title(self, title):
        if type(title) == str:
            for i in range(len(self.web_driver.window_handles)):
                self.web_driver.switch_to.window(self.web_driver.window_handles[i])
                if self.web_driver.title == title:
                    break   
        else:
            raise Exception("Invaild argument(title)...")
