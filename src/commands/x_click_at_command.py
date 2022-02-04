"""
Copyright (C) 2022 TestWorks Inc.
2022-01-22: (changsin@) created.
"""

import ctypes
import os
import random

if os.name == "posix":
    import autopy
import time

from enum import Enum
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

class Action(Enum):
    DRAW_BOX = "draw_box"
    SELECT_BOX = "select_box"
    RESIZE_BOX = "resize_box"


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

    screen_x = ((element_width * image_x) / image_width) + offset_x
    screen_y = ((element_height * image_y) / image_height) + offset_y

    return screen_x, screen_y


def clamp(n, smallest, largest): return max(smallest, min(n, largest))


def to_move(x, y, x_range, y_range, offsets, element_res):
    offset_x, offset_y = offsets
    element_width, element_height = element_res
    # direction = random.randint(1, 2)
    # if direction == 2:
    #     direction = -1
    lower_bound_x = offset_x - x
    upper_bound_x = element_width - x

    lower_bound_y = offset_y - y
    upper_bound_y = element_height - y

    move_x = random.randint(-x_range, x_range)
    move_y = random.randint(-y_range, y_range)

    move_x = clamp(move_x, lower_bound_x, upper_bound_x)
    move_y = clamp(move_y, lower_bound_y, upper_bound_y)

    return move_x, move_y


def draw_box(to_click_x, to_click_y, to_move_x=0, to_move_y=0):
    """
    MOUSE_LEFTDOWN = 0x0002     # left button down
    MOUSE_LEFTUP = 0x0004       # left button up
    MOUSE_RIGHTDOWN = 0x0008    # right button down
    MOUSE_RIGHTUP = 0x0010      # right button up
    MOUSE_MIDDLEDOWN = 0x0020   # middle button down
    MOUSE_MIDDLEUP = 0x0040     # middle button up
    """
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
        time.sleep(0.5)
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left down

        logger.info("Move {},{}".format(to_move_x, to_move_y))
        ctypes.windll.user32.mouse_event(1, to_move_x, to_move_y, 0, 0)
        time.sleep(0.5)

        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
        # need some time to move
        time.sleep(0.5)
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left down
    else:
        logger.warning("OS is " + os.name)


def select_box(to_click_x, to_click_y, to_move_x=10, to_move_y=10):
    """
    """
    if os.name == "posix":
        autopy.mouse.move(to_click_x, to_click_y)
        autopy.mouse.click()
    elif os.name == "nt":
        ctypes.windll.user32.SetCursorPos(to_click_x + to_move_x, to_click_y + to_move_y)
        time.sleep(0.5)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left down
    else:
        logger.warning("OS is " + os.name)


def resize_box(to_click_x, to_click_y, to_move_x=0, to_move_y=0):
    """
    """
    if os.name == "posix":
        autopy.mouse.move(to_click_x, to_click_y)
        autopy.mouse.click()
    elif os.name == "nt":
        ctypes.windll.user32.SetCursorPos(to_click_x, to_click_y)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
        # need some time to move
        time.sleep(0.5)

        logger.info("Move {},{}".format(to_move_x, to_move_y))
        ctypes.windll.user32.mouse_event(1, to_move_x, to_move_y, 0, 0)
        time.sleep(0.5)

        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left down
    else:
        logger.warning("OS is " + os.name)


def get_current_frame_number(web_driver):
    cur_frame = web_driver.find_element_by_id('currentFrameNumber')
    return int(cur_frame.get_attribute("value"))


class XClickAtCommand(Command):
    def execute(self):

        to_click_x, to_click_y = 0, 0
        object_number = 0

        logger.info("--->Before")
        visible_boxes = self.get_cur_boxes()
        cur_frame = get_current_frame_number(self.web_driver)

        (offset_x, offset_y), (width_el, height_el) = get_element_offsets_res(self.web_driver, self.target)
        (offset_viewport_x, offset_viewport_y) = get_viewport_offsets(self.web_driver)

        offset_x += offset_viewport_x
        offset_y += offset_viewport_y

        if self.value and len(self.value) > 0 and self.value != RANDOM:
            to_click_x, to_click_y = self.value.split(",")
        else:
            if self.test_option and (self.test_option == Action.SELECT_BOX.value or self.test_option == Action.RESIZE_BOX.value):
                id_to_click = random.randint(0, len(visible_boxes) - 1)
                # if safe_get_dict_item(self.test_data, "clicked"):
                #     if id_to_click in safe_get_dict_item(self.test_data, "clicked"):
                #         id_to_click += 1

                box = visible_boxes[id_to_click]
                logger.info(box)
                object_number, outside, occluded, points = box
                xtl, ytl, xbr, ybr = points

                to_click_x, to_click_y = to_screen((xtl, ytl), (offset_x, offset_y),
                                                   (width_el, height_el))
                # xbr_screen, ybr_screen = to_screen((xbr, ybr), (offset_x, offset_y),
                #                                    (width_el, height_el))
            else:
                x = random.randint(0, int(width_el - offset_x))
                y = random.randint(0, int(height_el - offset_y))

                to_click_x, to_click_y = to_screen((x, y), (offset_x, offset_y),
                                                   (width_el, height_el))

        to_move_x, to_move_y = to_move(to_click_x, to_click_y, 50, 50, (offset_x, offset_y), (width_el, height_el))

        if self.test_option:
            if self.test_option == Action.SELECT_BOX.value:
                select_box(int(to_click_x), int(to_click_y), int(to_move_x), int(to_move_y))
            elif self.test_option == Action.RESIZE_BOX.value:
                resize_box(int(to_click_x + 1), int(to_click_y + 1), int(to_move_x), int(to_move_y))
        else:
            draw_box(int(to_click_x), int(to_click_y), int(to_move_x), int(to_move_y))

        self.add_clicked(int(object_number))
        logger.info("### Click object_number={} at {},{} on frame={} ###".format(object_number,
                                                                                 to_click_x, to_click_y,
                                                                                 cur_frame))

        time.sleep(0.1)

        self.test_data["boxes"] = self.get_cur_boxes()
        logger.info("<---After")

        return True
