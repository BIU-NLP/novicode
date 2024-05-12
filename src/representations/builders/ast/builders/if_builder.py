from ast import *
from representations.builders.ast.builders.base_builder import BaseBuilder
from representations.tree.node import Node
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class IfBuilder(BaseBuilder):
    def build(self, root_item):
        name = type(root_item).__name__
        node = Node(name)

        # test
        test_node = Node("test")
        node.add_child(test_node, "test")
        test_chile_node = self.get_node(root_item.test)
        test_node.add_child(test_chile_node)

        # body
        body_node = Node("body")
        node.add_child(body_node)
        for body_item in root_item.body:
            body_child_node = self.get_node(body_item)
            body_node.add_child(body_child_node, "body")

        # or else
        if hasattr(root_item, "orelse") and len(root_item.orelse) > 0:
            or_else_node = Node("orelse")
            node.add_child(or_else_node)

            for or_else_child in root_item.orelse:
                or_else_child_node = self.get_node(or_else_child)
                or_else_node.add_child(or_else_child_node, "orelse")

        return node

    def is_match(self, item):
        name = type(item).__name__
        return name == "If"
