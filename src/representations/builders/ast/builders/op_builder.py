from representations.builders.ast.builders.base_builder import BaseBuilder
from representations.tree.node import Node


class OpBuilder(BaseBuilder):
    def build(self, root_item):
        node = super().build(root_item)

        if hasattr(root_item, "left"):
            left_node = self.get_node(root_item.left)
            node.add_child(left_node, "left")

        op_node = self.get_node(root_item.op)
        node.add_child(op_node, "op")

        if hasattr(root_item, "right"):
            right_node = self.get_node(root_item.right)
            node.add_child(right_node, "right")

        if hasattr(root_item, "operand"):
            operand_node = self.get_node(root_item.operand)
            node.add_child(operand_node, "operand")

        if hasattr(root_item, "values"):
            values_node = Node("values")
            node.add_child(values_node, "values")
            for value in root_item.values:
                value_node = self.get_node(value)
                values_node.add_child(value_node, "values")

        return node

    def is_match(self, item):
        name = type(item).__name__
        return name in ["UnaryOp", "BinOp", "BoolOp"]
