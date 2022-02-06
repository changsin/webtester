"""
Copyright (C) 2020 TestWorks Inc.

2020-03-05: changsin@ created as a POC
"""
from typing import List

from src.model.node.node import Node
from src.util import util


class TestCase:
    def __init__(self, name, url, nodes: List[Node]):
        self.name = name
        self.url = url
        self.nodes = nodes

    # TODO: this is a hacky way of serializing a test case.
    #   The problem is double escaping the json elements: especially nodes.
    #   when used with json.dumps() they are considered as strings
    #   A proper way is to implement JSON encoder and decoder
    def __str__(self):
        nodes_string = ""
        for idx, node in enumerate(self.nodes):
            if idx == len(self.nodes) - 1:
                nodes_string = nodes_string + node.to_json()
            else:
                nodes_string = nodes_string + node.to_json() + ","

        return "{ \"name\": \"%s\", \"url\": \"%s\", \"nodes\": [ %s ] }" % \
               (self.name, self.url, nodes_string)

    def to_json(self):
        return self.__str__()

    @staticmethod
    def from_json(json_dict):
        name = util.safe_get_dict_item(json_dict, 'name')
        url = util.safe_get_dict_item(json_dict, 'url')
        node_steps = []
        for js in json_dict['nodes']:
            node_steps.append(Node.from_json(js))

        return TestCase(name,
                        url,
                        node_steps)
