from typing import Any
import importlib
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class ArgTearer:
    def is_match(self, node: Node) -> bool:
        raise node.label == "arg"

    def tear(self, node: Node) -> Any:
        if node.children:
            class_name = node.label
            cls = getattr(importlib.import_module("ast"), class_name)

            # value
            factory = TearerFactory()
            tearer = factory.get_tearer(node.children[0])
            value = tearer.tear(node.children[0])

            return cls(value=value, lineno=None)
