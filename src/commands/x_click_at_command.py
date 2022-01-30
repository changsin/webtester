"""
Copyright (C) 2022 TestWorks Inc.
2022-01-22: (changsin@) created.
"""

import os
import ctypes
import random

if os.name == "posix":
    import autopy
import time

from src.util.logger import get_logger
from src.util.util import safe_get_dict_item

from .command import Command

logger = get_logger(__name__)


class XClickAtCommand(Command):
    def execute(self):
        if self.value and len(self.value) > 0:
            x, y = self.value.split(",")
            x = int(x)
            y = int(y)
        # logger.info("clickAt: {} {} {}".format(self.target, x, y))

        # TODO: get the original image resolutions dynamically from the proper source
        image_width = 1920
        image_height = 1080

        # TODO: need to translate image coordiantes to screen coordinates
        frame_grid = self.web_driver.find_element_by_id('frameGrid')
        offset_x = frame_grid.rect['x']
        offset_y = frame_grid.rect['y']
        frame_width = frame_grid.rect['width']
        frame_height = frame_grid.rect['height']

        # Assume all the browser chrome is on the top of the screen and none on the bottom.
        script_offset_x = "return window.screenX + (window.outerWidth - window.innerWidth) / 2 - window.scrollX;"
        script_offset_y = "return window.screenY + (window.outerHeight - window.innerHeight) - window.scrollY;"
        viewport_offset_x = self.web_driver.execute_script(script_offset_x)
        viewport_offset_y = self.web_driver.execute_script(script_offset_y)

        # logger.info("canvas x, y offset {},{}".format(viewport_offset_x, viewport_offset_y))

        browser_location = self.web_driver.get_window_position()
        # logger.info("browser_location {}".format(browser_location))
        offset_x += viewport_offset_x
        offset_y += viewport_offset_y

        logger.info("--->Before")
        visible_boxes = self.get_cur_boxes()

        id_to_click = random.randint(0, len(visible_boxes))
        if safe_get_dict_item(self.test_data, "clicked"):
            if id_to_click in safe_get_dict_item(self.test_data, "clicked"):
                id_to_click += 1

        visible_boxes_framed = []
        for box in visible_boxes:
            object_number, outside, occluded, points = box
            xtl, ytl, xbr, ybr = points
            xtl_framed = (frame_width * xtl)/image_width + offset_x
            ytl_framed = (frame_height * ytl)/image_height + offset_y
            xbr_framed = (frame_width * xbr)/image_width + offset_x
            ybr_framed = (frame_height * ybr)/image_height + offset_y

            visible_boxes_framed.append((object_number,
                                         [xtl_framed, ytl_framed, xbr_framed, ybr_framed]))

        # logger.info(visible_boxes_framed)
        for id, box in enumerate(visible_boxes_framed):
            if id == id_to_click:
                object_number, points = box
                xtl, ytl, xbr, ybr = points

                to_click_x = int(xtl) + 1
                to_click_y = int(ytl) + 1

                self.add_clicked(int(object_number))
                cur_frame = self.web_driver.find_element_by_id('currentFrameNumber')
                cur_frame = int(cur_frame.get_attribute("value"))
                logger.info("### Click object_number={} at {},{} on frame={} ###".format(object_number,
                                                                                       to_click_x, to_click_y,
                                                                                       cur_frame))

                # logger.info("frameGrid x={}, y={}, width={}, height={}".format(offset_x, offset_y, frame_width, frame_height))

                # ctypes.windll.user32.SetCursorPos(int(offset_x), int(offset_y))
                # ctypes.windll.user32.SetCursorPos(int(frame_width), int(frame_height))
                # logger.info("clickAt {},{}".format(to_click_x, to_click_y))

                if os.name == "posix":
                    autopy.mouse.move(to_click_x, to_click_y)
                    autopy.mouse.click()
                elif os.name == "nt":
                    ctypes.windll.user32.SetCursorPos(to_click_x, to_click_y)
                    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
                    # need some time to move
                    time.sleep(0.1)

                    direction = random.randint(1, 2)
                    if direction == 2:
                        direction = -1
                    move_x = random.randint(0, 15) * direction
                    move_y = random.randint(0, 15) * direction

                    logger.info("Move {},{}".format(move_x, move_y))
                    ctypes.windll.user32.mouse_event(1, move_x, move_y, 0, 0)
                    time.sleep(0.1)
                    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up
                else:
                    logger.warning("OS is " + os.name)

        time.sleep(0.1)

        self.test_data["boxes"] = self.get_cur_boxes()
        logger.info("<---After")

        return True
