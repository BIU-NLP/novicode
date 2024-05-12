from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class ListCompTearer(BaseTearer):
    def is_match(self, node):
        return node.label in ["ListComp"]

    def tear(self, node: Node) -> Any:
        factory = TearerFactory()

        # elt
        elt = factory.get_tearer(node.children[0]).tear(node.children[0])

        # generators
        iter_item = factory.get_tearer(node.children[1]).tear(node.children[1])
        target = factory.get_tearer(node.children[2]).tear(node.children[2])
        generators = [
            comprehension(iter=iter_item, target=target, ifs=None, is_async=None)
        ]

        return ListComp(elt=elt, generators=generators, lineno=None)
