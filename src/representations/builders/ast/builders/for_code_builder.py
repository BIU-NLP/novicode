import ast
from representations.tree.node import Node
from representations.builders.ast.builders.base_builder import BaseBuilder


class ForBuilder(BaseBuilder):
    def build(self, root_item):
        name = type(root_item).__name__
        node = Node(name)

        # iter + target
        test_node = Node("test")
        node.add_child(test_node)

        if hasattr(root_item, "iter"):
            iter_node = Node("iter")
            test_node.add_child(iter_node)
            iter_text = ast.unparse(root_item.iter)
            iter_child_node = Node(iter_text)
            iter_node.add_child(iter_child_node, "iter")

        # target
        if hasattr(root_item, "target"):
            target_node = self.get_node(root_item.target)
            test_node.add_child(target_node, "target")

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
        return (super().get_priority() + (1 if self.rules_enabled else -1))

    def is_match(self, item):
        name = type(item).__name__
        return name == "For"

    def _is_ast_match(self, item):
        return type(item).__name__ in [
            "Assign",
            "AugAssign",
            "AnnAssign",
            "Call",
            "Expr",
        ]
