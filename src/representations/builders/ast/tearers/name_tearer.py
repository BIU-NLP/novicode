from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class NameTearer(BaseTearer):
    def is_match(self, node):
        return node.label == "Name"

    def tear(self, node: Node) -> Any:
        return Name(id=node.children[0].label, ctx=Load(), lineno=None)
