from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class ListTearer(BaseTearer):
    def is_match(self, node):
        return node.label == "List"

    def tear(self, node: Node) -> Any:
        factory = TearerFactory()
        return List(
            elts=[factory.get_tearer(child).tear(child) for child in node.children],
            ctx=Load(),
            lineno=None,
        )
