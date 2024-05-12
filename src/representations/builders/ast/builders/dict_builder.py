from representations.builders.ast.builders.base_builder import BaseBuilder
from representations.tree.node import Node


class DictBuilder(BaseBuilder):
    def build(self, root_item):
        node = super().build(root_item)

        for i, (key, value) in enumerate(zip(root_item.keys, root_item.values)):
            key_value_node = Node(f"{i}")
            node.add_child(key_value_node, "key_value")

            key_node = Node("key")
            key_value_node.add_child(key_node, "key")
            key_node_child = self.get_node(key)
            key_node.add_child(key_node_child)

            value_node = Node("value")
            key_value_node.add_child(value_node, "value")
            value_node_child = self.get_node(value)
            value_node.add_child(value_node_child)

        return node
    
    def is_match(self, item):
        name = type(item).__name__
        return name == "Dict"
