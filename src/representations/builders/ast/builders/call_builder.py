from representations.builders.ast.builders.base_builder import BaseBuilder
from representations.tree.node import Node


class CallBuilder(BaseBuilder):
    def build(self, root_item):
        node = super().build(root_item)

        # func
        func_node = Node("func")
        node.add_child(func_node)
        func_child_node = self.get_node(root_item.func)
        func_node.add_child(func_child_node, "func")

        # args
        if hasattr(root_item, "args") and len(root_item.args) > 0:
            for arg_item in root_item.args:
                arg_node = Node("arg")
                node.add_child(arg_node)
                arg_child_node = self.get_node(arg_item)
                arg_node.add_child(arg_child_node, "args")

        # keywords
        if hasattr(root_item, "keywords") and len(root_item.keywords) > 0:
            for keyword_item in root_item.keywords:
                keywords_node = self.get_node(keyword_item)
                node.add_child(keywords_node, "keywords")

        return node

    def is_match(self, item):
        name = type(item).__name__
        return name == "Call"
