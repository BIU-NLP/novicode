from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class AttributeTearer(BaseTearer):
    def is_match(self, node):
        return node.label == "Dict"

    def tear(self, node: Node) -> Any:
        factory = TearerFactory()
        keys = []
        values = []
        for child in node.children:
            # key
            key_node = child.children[0].children[0]
            tearer = factory.get_tearer(key_node)
            key = tearer.tear(key_node)
            keys.append(key)
            # value
            value_node = child.children[1].children[0]
            tearer = factory.get_tearer(value_node)
            value = tearer.tear(value_node)
            values.append(value)

        return Dict(keys=keys, values=values, lineno=None)
