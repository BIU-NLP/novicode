import ast
from ast import *
from representations.builders.ast.builders.base_builder import BaseBuilder
from representations.tree.node import Node
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class IfCodeBuilder(BaseBuilder):
    def build(self, root_item):
        name = type(root_item).__name__
        node = Node(name)

        # test
        test_node = Node("test")
        node.add_child(test_node, "test")
        test_text = ast.unparse(root_item.test)
        test_chile_node = Node(test_text)
        test_node.add_child(test_chile_node)

        # body
        body_node = Node("body")
        node.add_child(body_node)
        for body_item in root_item.body:
            if self._is_ast_match(body_item):
                body_child_text = ast.unparse(body_item)
                body_child_node = Node(body_child_text)
            else:
                body_child_node = self.get_node(body_item)
            body_node.add_child(body_child_node, "body")

        # or else
        if hasattr(root_item, "orelse") and len(root_item.orelse) > 0:
            or_else_node = Node("orelse")
            node.add_child(or_else_node)
            for or_else_item in root_item.orelse:
                if self._is_ast_match(or_else_item):
                    or_else_child_text = ast.unparse(or_else_item)
                    or_else_child_node = Node(or_else_child_text)
                else:
                    or_else_child_node = self.get_node(or_else_item)
                or_else_node.add_child(or_else_child_node, "orelse")

        return node

    def get_priority(self):
        return (super().get_priority() + (1 if self.rules_enabled else -1))

    def is_match(self, item):
        name = type(item).__name__
        return name == "If"

    def _is_ast_match(self, item):
        return type(item).__name__ in [
            "Assign",
            "AugAssign",
            "AnnAssign",
            "Call",
            "Expr",
        ]
