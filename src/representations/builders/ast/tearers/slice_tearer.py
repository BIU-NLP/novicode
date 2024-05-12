from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class SliceTearer(BaseTearer):
    def is_match(self, node):
        return node.label == "Slice"

    def tear(self, node: Node) -> Any:
        factory = TearerFactory()

        # lower
        if node.get_children(label="lower", direct=True):
            value_node = node.get_children(label="lower", direct=True)[0]
            lower = factory.get_tearer(value_node.children[0]).tear(
                value_node.children[0]
            )
        else:
            lower = None

        # upper
        if node.get_children(label="upper", direct=True):
            value_node = node.get_children(label="upper", direct=True)[0]
            upper = factory.get_tearer(value_node.children[0]).tear(
                value_node.children[0]
            )
        else:
            upper = None

        return Slice(lower=lower, upper=upper, step=None)
