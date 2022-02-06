class Command:
    def __init__(self, command, target, value):
        self.command = command
        self.target = target
        self.value = value

    def __str__(self):
        return "{\"Command\": \"%s\", \"Target\": \"%s\", \"Value\": \"%s\"}" % \
                (self.command, self.target, self.value)

    def to_json(self):
        return self.__str__()

    # TODO: add other commands and targets
    @staticmethod
    def from_json(node):
        if type(node) is not dict:
            command = node.action.value
            # target is ambiguous. so, change target to xpath. if command is 'open', insert url in target
            target = "xpath=" + str(node.xpath).replace("\\", "")
            value = node.value
            node_type = node.tag

            if command == "open":
                target = node.url
                value = ""
            elif command == "mouse_move":
                command = "mouseOver"

            if node_type == "select_option":
                command = "select"
        else:
            command = node["Command"]
            target = node["Target"]
            value = node["Value"]

        # value가 None으로 저장되는 버그 수정(7/8)
        value = value if (value is not None) else ""
        return Command(command, target, value)
