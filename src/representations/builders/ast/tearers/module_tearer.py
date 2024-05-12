from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class ModuleTearer(BaseTearer):
    def is_match(self, node):
        return node.label == "Module"

    def tear(self, node: Node) -> Any:
        factory = TearerFactory()

        # body
        body = None
        if node.children and len(node.children) > 0:
            body = []
            for child in node.children:
                tearer = factory.get_tearer(child)
                item = tearer.tear(child)
                body.append(item)

        return Module(body=body, type_ignores=[], lineno=None)
