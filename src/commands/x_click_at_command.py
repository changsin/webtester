"""
Copyright (C) 2022 TestWorks Inc.
2022-01-22: (changsin@) created.
"""

import ctypes
import autopy
import time

from src.util.logger import get_logger
from .command import Command

logger = get_logger(__name__)


class XClickAtCommand(Command):
    def get_cur_boxes(self):
        """
        :return: bounding boxes of the current frame
        """
        script = """
            return {...window.cvat.data.get()};
            """
        collected = self.web_driver.execute_script(script)
        cur_frame = self.web_driver.find_element_by_id('currentFrameNumber')
        cur_frame = int(cur_frame.get_attribute("value"))

        tracks = collected['tracks']

        tracks_to_track = []
        for track in tracks:
            if cur_frame >= track['frame']:
                tracks_to_track.append(track)

        visible_boxes = []
        for track in tracks_to_track:
            shapes = track['shapes']
            shape_last = None
            for shape in shapes:
                if shape['frame'] <= cur_frame:
                    shape_last = shape
                    continue

                if not shape_last['outside']:
                    points = shape_last['points']
                    object_number = track['object_number']
                    visible_boxes.append((object_number, points))
                    break

        logger.info(visible_boxes)

        return visible_boxes

    def execute(self):
        x, y = self.value.split(",")
        x = int(x)
        y = int(y)
        logger.info("clickAt: {} {} {}".format(self.target, x, y))

        # TODO: get the original image resolutions dynamically from the proper source
        image_width = 1920
        image_height = 1080

        autopy.mouse.move(x, y)
        autopy.mouse.click()

        # TODO: need to translate image coordiantes to screen coordinates
        frame_grid = self.web_driver.find_element_by_id('frameGrid')
        offset_x = frame_grid.rect['x']
        offset_y = frame_grid.rect['y']
        frame_width = frame_grid.rect['width']
        frame_height = frame_grid.rect['height']

        visible_boxes = self.get_cur_boxes()

        visible_boxes_framed = []
        for box in visible_boxes:
            object_number, points = box
            xtl, ytl, xbr, ybr = points
            xtl_framed = (frame_width * xtl)/image_width + offset_x
            ytl_framed = (frame_height * ytl)/image_height + offset_y
            xbr_framed = (frame_width * xbr)/image_width + offset_x
            ybr_framed = (frame_height * ybr)/image_height + offset_y

            visible_boxes_framed.append((object_number,
                                         [xtl_framed, ytl_framed, xbr_framed, ybr_framed]))

        logger.info(visible_boxes_framed)

        for box in visible_boxes_framed:
            object_number, points = box
            xtl, ytl, xbr, ybr = points

            # autopy.mouse.move(int(xtl), int(ytl))
            autopy.mouse.move(int(frame_width), int(frame_height) - 100)
            time.sleep(3)
            autopy.mouse.click()

        # This works only in Windows
        # ctypes.windll.user32.SetCursorPos(x, y)
        # ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
        # ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up

        time.sleep(2)

        return True
