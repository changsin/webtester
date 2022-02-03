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

from src.util.selenium_util import get_element
from src.util.logger import get_logger
from src.util.util import safe_get_dict_item

from .command import Command

logger = get_logger(__name__)

# TODO: get the original image resolutions dynamically from the proper source
HD_WIDTH = 1920
HD_HEIGHT = 1080

HD_RES = (HD_WIDTH, HD_HEIGHT)
RANDOM = "{RANDOM}"


def get_viewport_offsets(web_driver):
    # Assume all the browser chrome is on the top of the screen and none on the bottom.
    script_viewport_x = "return window.screenX + (window.outerWidth - window.innerWidth) / 2 - window.scrollX;"
    script_viewport_y = "return window.screenY + (window.outerHeight - window.innerHeight) - window.scrollY;"
    offset_viewport_x = web_driver.execute_script(script_viewport_x)
    offset_viewport_y = web_driver.execute_script(script_viewport_y)

    return offset_viewport_x, offset_viewport_y


def get_element_offsets_res(web_driver, target):
    element = get_element(web_driver, target)
    offset_x = element.rect['x']
    offset_y = element.rect['y']
    width = element.rect['width']
    height = element.rect['height']

    return (offset_x, offset_y), (width, height)


def to_screen(pt_image, offsets, element_res, image_res=HD_RES):
    image_x, image_y = pt_image
    offset_x, offset_y = offsets
    element_width, element_height = element_res
    image_width, image_height = image_res

    screen_x = (element_width * image_x) / image_width + offset_x
    screen_y = (element_height * image_y) / image_height + offset_y

    return screen_x, screen_y


def click_at(to_click_x, to_click_y):
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
        move_x = random.randint(0, 20) * direction
        move_y = random.randint(0, 20) * direction

        logger.info("Move {},{}".format(move_x, move_y))
        ctypes.windll.user32.mouse_event(1, move_x, move_y, 0, 0)
        time.sleep(0.1)
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up
    else:
        logger.warning("OS is " + os.name)


class XClickAtCommand(Command):
    def execute(self):

        to_click_x, to_click_y = 0, 0
        object_number = 0

        cur_frame = self.web_driver.find_element_by_id('currentFrameNumber')
        cur_frame = int(cur_frame.get_attribute("value"))

        logger.info("--->Before")
        visible_boxes = self.get_cur_boxes()

        if self.value and len(self.value) > 0 and self.value != RANDOM:

            x, y = self.value.split(",")
            to_click_x = int(x)
            to_click_y = int(y)
        else:
            (offset_x, offset_y), (element_width, element_height) = get_element_offsets_res(self.web_driver,
                                                                                            self.target)
            (offset_viewport_x, offset_viewport_y) = get_viewport_offsets(self.web_driver)

            offset_x += offset_viewport_x
            offset_y += offset_viewport_y

            id_to_click = random.randint(0, len(visible_boxes))
            if safe_get_dict_item(self.test_data, "clicked"):
                if id_to_click in safe_get_dict_item(self.test_data, "clicked"):
                    id_to_click += 1

            for id, box in enumerate(visible_boxes):
                if id == id_to_click:
                    logger.info(box)
                    object_number, outside, occluded, points = box
                    xtl, ytl, xbr, ybr = points

                    xtl_screen, ytl_screen = to_screen((xtl, ytl), (offset_x, offset_y),
                                                       (element_width, element_height))
                    xbr_screen, ybr_screen = to_screen((xbr, ybr), (offset_x, offset_y),
                                                       (element_width, element_height))
                    to_click_x = int(xtl_screen) + 1
                    to_click_y = int(xbr_screen) + 1

                    break

        click_at(to_click_x, to_click_y)
        self.add_clicked(int(object_number))
        logger.info("### Click object_number={} at {},{} on frame={} ###".format(object_number,
                                                                                 to_click_x, to_click_y,
                                                                                 cur_frame))

        time.sleep(0.1)

        self.test_data["boxes"] = self.get_cur_boxes()
        logger.info("<---After")

        return True
