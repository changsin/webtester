"""
Copyright (C) 2020 TestWorks Inc.
"""
from abc import ABC, abstractmethod
from src.util.logger import get_logger
from src.util.util import safe_get_dict_item

logger = get_logger(__name__)


class Command(ABC):
    def __init__(self, web_driver, target, value, env, os_ver, browser, browser_version, test_option):
        self.web_driver = web_driver
        self.target = target
        self.value = value
        self.env = env
        self.os_ver = os_ver
        self.browser = browser
        self.browser_version = browser_version
        self.test_option = test_option
        self.test_data = {}

    def add_clicked(self, id):
        if safe_get_dict_item(self.test_data, "clicked"):
            self.test_data["clicked"].append(id)
        else:
            self.test_data["clicked"] = [id]

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    def get_cur_boxes(self):
        """
        :return: bounding boxes of the current frame
        """
        script = """
            function getSafe(defaultVal) {
              try {
                return {...window.cvat.data.get()};
              } catch (e) {
                return defaultVal;
              }
            }
            console.log("log");
            return getSafe("undefined");
            """
        collected = self.web_driver.execute_script(script)
        # logger.info("collected {}".format(collected))
        if "undefined" == collected:
            return None

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
                # only consider if the started frame is before the currrent frame
                if shape['frame'] <= cur_frame:
                    shape_last = shape
                    continue

                if not shape_last['outside']:
                    object_number = track['object_number']
                    points = shape_last['points']
                    visible_boxes.append((object_number,
                                          shape_last['outside'],
                                          shape_last['occluded'],
                                          points))
                    break

        idx_visible = []
        for id, outside, occluded, points in visible_boxes:
            idx_visible.append(id)

        logger.info("visible idx: {}".format(idx_visible))

        idx_all = []
        for track in tracks:
            object_number = track['object_number']
            shapes = []
            for shape in track['shapes']:
                shapes.append({"object_number": object_number,
                               "frame": shape['frame'],
                               "outside": shape['outside'],
                               "occluded": shape['occluded'],
                               "z_order": shape['z_order']})

            idx_all.append({"object_number": track['object_number'],
                            "id": track['id'],
                            "select": track['select'],
                            "shapes": shapes})

        logger.info("all idx: {}".format(idx_all))

        return visible_boxes

