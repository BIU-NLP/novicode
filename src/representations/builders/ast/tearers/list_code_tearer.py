from typing import Any
import re
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class ListCodeTearer(BaseTearer):
    def is_match(self, node):
        return re.match(r"^\[.*\]$", node.label.strip())
    
    def get_priority(self) -> int:
        return super().get_priority() + (1 if self.rules_enabled else -1)

    def tear(self, node: Node) -> Any:
        factory = TearerFactory()
        return List(
            elts=[factory.get_tearer(child).tear(child) for child in node.children],
            ctx=Load(),
            lineno=None,
        )
