from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class AttributeTearer(BaseTearer):
    def is_match(self, node):
        return node.label == "Attribute"

    def tear(self, node: Node) -> Any:
        # value
        value = TearerFactory().get_tearer(node.children[0]).tear(node.children[0])

        # attr
        attr = node.children[1].label

        return Attribute(value=value, attr=attr, ctx=Load(), lineno=None)
