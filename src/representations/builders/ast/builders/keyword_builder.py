from representations.builders.ast.builders.base_builder import BaseBuilder
from representations.tree.node import Node


class KeywordBuilder(BaseBuilder):
    def build(self, root_item):
        name = type(root_item).__name__
        node = Node(name)

        # func
        arg_node = Node("arg")
        node.add_child(arg_node, "arg")
        arg_child_node = Node(root_item.arg)
        arg_node.add_child(arg_child_node, "arg")

        # keywords
        if hasattr(root_item, "value"):
            value_node = self.get_node(root_item.value)
            node.add_child(value_node, "value")

        return node
    
    def is_match(self, item):
        name = type(item).__name__
        return name == "keyword"
