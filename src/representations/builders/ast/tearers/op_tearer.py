from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class OpTearer(BaseTearer):
    def is_match(self, node):
        return node.label in ["BoolOp", "BinOp", "UnaryOp"]

    def tear(self, node: Node) -> Any:
        factory = TearerFactory()

        if node.label == "BinOp":
            # left
            left = (
                factory.get_tearer(node.children[0]).tear(node.children[0])
                if node.children and len(node.children) > 0
                else None
            )
            # op
            op = self.tear_bin_op_op(node.children[1])

            # right
            right = (
                factory.get_tearer(node.children[2]).tear(node.children[2])
                if node.children and len(node.children) > 2
                else None
            )

            return BinOp(left=left, op=op, right=right, lineno=None)

        elif node.label == "BoolOp":
            # op
            if node.children[0].label == "Or":
                op = Or()
            elif node.children[0].label == "And":
                op = And()
            else:
                op = None

            # values
            if (
                len(node.children) > 1
                and node.children[1].label == "values"
                and len(node.children[1].children) > 0
            ):
                values = []
                for child in node.children[1].children:
                    tearer = factory.get_tearer(child)
                    value = tearer.tear(node.children[1])
                    values.append(value)

            return BoolOp(op=op, values=values, lineno=None)
        elif node.label == "UnaryOp":
            # op
            if node.children[0].label == "Invert":
                op = Invert()
            elif node.children[0].label == "Not":
                op = Not()
            elif node.children[0].label == "UAdd":
                op = UAdd()
            elif node.children[0].label == "USub":
                op = USub()
            else:
                op = None

            # operand
            tearer = factory.get_tearer(node.children[1])
            operand = tearer.tear(node.children[1])

            return UnaryOp(op=op, operand=operand, lineno=None)

    def tear_bin_op_op(self, op_node):
        if op_node.label == "Add":
            op = Add()
        elif op_node.label == "Sub":
            op = Sub()
        elif op_node.label == "Mult":
            op = Mult()
        elif op_node.label == "MatMult":
            op = Mult()
        elif op_node.label == "Div":
            op = Div()
        elif op_node.label == "Mod":
            op = Mod()
        elif op_node.label == "Pow":
            op = Pow()
        elif op_node.label == "LShift":
            op = LShift()
        elif op_node.label == "RShift":
            op = RShift()
        elif op_node.label == "BitOr":
            op = RShift()
        elif op_node.label == "BitXor":
            op = RShift()
        elif op_node.label == "BitAnd":
            op = RShift()
        elif op_node.label == "FloorDiv":
            op = FloorDiv()
        else:
            op = None

        return op
