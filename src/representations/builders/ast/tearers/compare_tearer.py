from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class ComapreTearer(BaseTearer):
    def is_match(self, node):
        return node.label in ["Compare"]

    def tear(self, node: Node) -> Any:
        factory = TearerFactory()

        # left
        left_node = node.children[0]
        tearer = factory.get_tearer(left_node)
        left = tearer.tear(left_node)

        # ops
        ops_node = node.children[1]
        ops = [self.tear_ops(ops_node)]

        # comparators
        comparators_node = node.children[2]
        comparators = [
            factory.get_tearer(comparators_node).tear(comparators_node)
        ]

        return Compare(left=left, ops=ops, comparators=comparators, lineno=None)

    def tear_ops(self, node: Node) -> Any:
        if node.label == "Eq":
            return Eq()
        elif node.label == "NotEq":
            return NotEq()
        elif node.label == "Lt":
            return Lt()
        elif node.label == "LtE":
            return LtE()
        elif node.label == "Gt":
            return Gt()
        elif node.label == "GtE":
            return GtE()
        elif node.label == "Is":
            return Is()
        elif node.label == "IsNot":
            return IsNot()
        elif node.label == "In":
            return In()
        elif node.label == "NotIn":
            return NotIn()
        else:
            return None
