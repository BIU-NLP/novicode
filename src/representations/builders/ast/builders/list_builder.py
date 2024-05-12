from representations.builders.ast.builders.base_builder import BaseBuilder
from representations.tree.node import Node


class ListBuilder(BaseBuilder):
    def build(self, root_item):
        node = super().build(root_item)

        for item in root_item.elts:
            item_node = self.get_node(item)
            node.add_child(item_node)

        return node

    def is_match(self, item):
        name = type(item).__name__
        return name == "List"
