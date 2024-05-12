from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class IfTearer(BaseTearer):
    def is_match(self, node):
        return node.label in ["If", "While"]

    def tear(self, node: Node) -> Any:
        factory = TearerFactory()

        # test
        test = None
        if (
            len(node.children) > 0
            and node.children[0].label == "test"
            and len(node.children[0].children) > 0
        ):
            test_node = node.children[0]
            tearer = factory.get_tearer(test_node.children[0])
            test = tearer.tear(test_node.children[0])

        # body
        body = []
        if (
            len(node.children) > 1
            and node.children[1].label == "body"
            and len(node.children[1].children) > 0
        ):
            body_node = node.children[1]
            for child in body_node.children:
                tearer = factory.get_tearer(child)
                item = tearer.tear(child)
                body.append(item)

        # orelse
        orelse = []
        if (
            len(node.children) > 2
            and node.children[2].label == "orelse"
            and len(node.children[2].children) > 0
        ):
            orelse_node = node.children[2]
            for child in orelse_node.children:
                tearer = factory.get_tearer(child)
                item = tearer.tear(child)
                orelse.append(item)

        return (
            If(test=test, body=body, orelse=orelse, lineno=None)
            if node.label == "If"
            else While(test=test, body=body, orelse=orelse, lineno=None)
        )
