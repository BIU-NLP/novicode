from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class DictCompTearer(BaseTearer):
    def is_match(self, node):
        return node.label in ["DictComp"]

    def tear(self, node: Node) -> Any:
        factory = TearerFactory()

        # key
        key = factory.get_tearer(node.children[0].children[0]).tear(
            node.children[0].children[0]
        )

        # value
        value = factory.get_tearer(node.children[1].children[0]).tear(
            node.children[1].children[0]
        )

        # generators
        iter_item = factory.get_tearer(node.children[2]).tear(node.children[2])
        target = factory.get_tearer(node.children[3]).tear(node.children[3])
        generators = [
            comprehension(iter=iter_item, target=target, ifs=None, is_async=None)
        ]

        return DictComp(key=key, value=value, generators=generators, lineno=None)
