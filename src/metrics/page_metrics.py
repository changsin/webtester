import json

from src.metrics.node_metrics import NodeMetrics
from src.util import util
from src.util.logger import get_logger
from src.util.serialize import default

logger = get_logger(__name__)


class PageMetrics:
    """
    node_metric is a dictionary of node_metrics whose key is the node type: e.g., { "button": <node_metrics>}
    The reason for using dict instead of class objects internally and for serialization is for readability.
    When it is serialized inside a NodePage which is included in a graph object,
    an object is serialized triple times and thus it becomes hard to read.
    """
    def __init__(self, node_metrics):
        self.node_metrics = node_metrics
        self.load_times = []
        self.parse_time = 0.0

    def __str__(self):
        return json.dumps(dict({
            "node_metrics": self.node_metrics,
            "load_times": self.load_times,
            "parse_time": self.parse_time
        }), default=default)

    def to_json(self):
        return self.__str__()

    @staticmethod
    def from_json(json_dict):
        page_metrics_obj = PageMetrics(None)
        page_metrics_obj.node_metrics = util.safe_get_dict_item(json_dict, "node_metrics")
        page_metrics_obj.load_times = util.safe_get_dict_item(json_dict, "load_times")
        page_metrics_obj.parse_time = util.safe_get_dict_item(json_dict, "parse_time")

        return page_metrics_obj

    def update_actionable_metrics(self, actionable):
        node_metrics_dict = util.safe_get_dict_item(self.node_metrics, actionable.tag)
        if node_metrics_dict:
            node_metrics_dict['actionable'] = node_metrics_dict['actionable'] + 1
            self.node_metrics[actionable.tag] = node_metrics_dict
        else:
            node_metrics = NodeMetrics()
            node_metrics.actionable = 1

        return self
