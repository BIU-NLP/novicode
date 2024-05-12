from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class IfTearer(BaseTearer):
    def is_match(self, node):
        return node.label == "Expr"
    
    def tear(self, node: Node) -> Any:
        factory = TearerFactory()
        
        # expr
        value = factory.get_tearer(node.children[0]).tear(node.children[0])

        return Expr(value=value, lineno=None)