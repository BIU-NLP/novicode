from representations.tree.node import Node
from representations.builders.ast.builders.base_builder import BaseBuilder


class LambdaBuilder(BaseBuilder):
    def build(self, root_item):
        name = type(root_item).__name__
        node = Node(name)

        # args
        if hasattr(root_item, "args"):
            arguments_node = Node("args")
            node.add_child(arguments_node)
            if hasattr(root_item.args, "args") and len(root_item.args.args) > 0:
                for args_item in root_item.args.args:
                    arg_child_node = self.get_node(args_item)
                    arguments_node.add_child(arg_child_node)

        # body
        if hasattr(root_item, "body"):
            body_node = Node("body")
            node.add_child(body_node)
            bodu_child_node = self.get_node(root_item.body)
            body_node.add_child(bodu_child_node)

        return node
    
    def is_match(self, item):
        name = type(item).__name__
        return name == "Lambda"
