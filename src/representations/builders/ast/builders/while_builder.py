from representations.builders.ast.builders.base_builder import BaseBuilder
from representations.tree.node import Node


class WhileBuilder(BaseBuilder):
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

        return node
    
    def is_match(self, item):
        name = type(item).__name__
        return name == "While"
