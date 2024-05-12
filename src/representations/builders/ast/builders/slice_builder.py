from representations.builders.ast.builders.base_builder import BaseBuilder
from representations.tree.node import Node


class SliceBuilder(BaseBuilder):
    def build(self, root_item):
        node = super().build(root_item)

        if hasattr(root_item, "lower"):
            lower_node = Node("lower")
            node.add_child(lower_node)
            lower_child_node = self.get_node(root_item.lower)
            lower_node.add_child(lower_child_node, "lower")

        if hasattr(root_item, "upper"):
            upper_node = Node("upper")
            node.add_child(upper_node)
            upper_child_node = self.get_node(root_item.upper)
            upper_node.add_child(upper_child_node, "upper")

        return node

    def is_match(self, item):
        name = type(item).__name__
        return name == "Slice"
