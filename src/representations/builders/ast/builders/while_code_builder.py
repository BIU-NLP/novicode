import ast
from representations.builders.ast.builders.base_builder import BaseBuilder
from representations.tree.node import Node


class WhileCodeBuilder(BaseBuilder):
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

        return node

    def get_priority(self):
        return super().get_priority() + (1 if self.rules_enabled else -1)

    def is_match(self, item):
        name = type(item).__name__
        return name == "While"
