"""
Copyright (C) 2022 TestWorks Inc.
2022-01-22: (changsin@) created.
"""

from src.util.selenium_util import get_element
from src.util.logger import get_logger
from .command import Command

logger = get_logger(__name__)


class XSnapshotCommand(Command):
    def execute(self):
        script = """
            return {...window.cvat.data.get()};
            """
        collected = self.web_driver.execute_script(script)

        # logger.info("class snapshot: {}".format(collected))

        # cur_frame = get_element(self.web_driver, 'currentFrameNumber')
        cur_frame = self.web_driver.find_element_by_id('currentFrameNumber')
        cur_frame = int(cur_frame.get_attribute("value"))

        tracks = collected['tracks']

        cur_objects = []
        for track in tracks:
            if cur_frame >= track['frame']:
                cur_objects.append(track)

        logger.info("Objects in the current frame are {}".format(len(cur_objects)))

        return True
