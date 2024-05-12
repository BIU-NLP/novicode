from representations.builders.ast import builders
from representations.tree.node import Node


class BaseBuilder:
    def __init__(self, rules_enabled: bool = False) -> None:
        super().__init__()
        self.rules_enabled = rules_enabled

    def build(self, root_item):
        name = type(root_item).__name__
        node = Node(name)

        if hasattr(root_item, "body"):
            self.build_body(root_item, node)

        elif hasattr(root_item, "targets") or hasattr(root_item, "target"):
            self.build_targets(root_item, node)

        if hasattr(root_item, "id"):
            self.build_id(root_item, node)

        if hasattr(root_item, "slice"):
            self.build_slice(root_item, node)

        if hasattr(root_item, "value"):
            self.build_value(root_item, node)

        if hasattr(root_item, "arg"):
            self.build_arg(root_item, node)

        return node

    def get_node(self, item):
        factory = builders.builder_factory.BuilderFactory()
        builder = factory.get_builder(item, rules_enabled=self.rules_enabled)
        node = builder.build(item)
        return node

    def get_priority(self):
        return 100

    def is_enabled(self):
        return True

    def build_arg(self, root_item, node) -> None:
        child_node = Node(root_item.arg)
        node.add_child(child_node, "arg")

    def build_body(self, root_item, node) -> None:
        for item in root_item.body:
            child_node = self.get_node(item)
            node.add_child(child_node, "body")

    def build_id(self, root_item, node) -> None:
        child_node = Node(root_item.id)
        node.add_child(child_node, "slice")

    def build_slice(self, root_item, node) -> None:
        child_node = self.get_node(root_item.slice)
        node.add_child(child_node, "slice")

    def build_targets(self, root_item, node) -> None:
        if hasattr(root_item, "targets"):
            for item in root_item.targets:
                child_node = self.get_node(item)
                node.add_child(child_node, "targets")
        elif hasattr(root_item, "target"):
            child_node = self.get_node(root_item.target)
            node.add_child(child_node, "target")

    def build_value(self, root_item, node) -> None:
        if type(root_item.value).__name__ in [
            "bool",
            "str",
            "int",
            "float",
        ]:
            type_node = Node(type(root_item.value).__name__)
            node.add_child(type_node, "value")
            value_node = Node(root_item.value)
            type_node.add_child(value_node)
        else:
            child_node = self.get_node(root_item.value)
            node.add_child(child_node, "value")
