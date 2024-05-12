from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class KeywordTearer(BaseTearer):
    def is_match(self, node):
        return node.label == "keyword"

    def tear(self, node: Node) -> Any:
        factory = TearerFactory()

        # arg
        arg_node = node.children[0]
        arg = arg_node.children[0].label

        # value
        value_node = node.children[1]
        value = factory.get_tearer(value_node).tear(value_node)

        return keyword(arg=arg, value=value, lineno=None)
