import json

from src.util import util


class NodeMetrics:
    def __init__(self):
        self.available = 0
        self.visible = 0
        self.filtered = 0
        self.actionable = 0

    def __str__(self):
        return json.dumps(dict({
            "available": self.available,
            "visible": self.visible,
            "filtered": self.filtered,
            "actionable": self.actionable
        }))

    def to_json(self):
        return self.__str__()

    @staticmethod
    def from_json(json_dict):
        node_metrics = NodeMetrics()
        node_metrics.available = util.safe_get_dict_item(json_dict, "available")
        node_metrics.visible = util.safe_get_dict_item(json_dict, "visible")
        node_metrics.filtered = util.safe_get_dict_item(json_dict, "filtered")
        node_metrics.actionable = util.safe_get_dict_item(json_dict, "actionable")

        return node_metrics
