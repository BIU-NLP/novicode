from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class ConstantTearer(BaseTearer):
    def is_match(self, node):
        return node.label == "Constant"

    def tear(self, node: Node) -> Any:
        if node.children[0].label == "bool":
            value = bool(node.children[0].children[0].label)
        elif node.children[0].label == "float":
            value = float(node.children[0].children[0].label)
        elif node.children[0].label == "int":
            value = int(node.children[0].children[0].label)
        elif node.children[0].label == "str":
            value = str(node.children[0].children[0].label)
        else:
            value = node.children[0].children[0].label

        return Constant(value=value, lineno=None)
