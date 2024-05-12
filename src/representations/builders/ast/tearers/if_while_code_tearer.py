from typing import Any
import ast
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class IfWhileCodeTearer(BaseTearer):
    def is_match(self, node):
        return node.label in ["If", "While"]

    def get_priority(self) -> int:
        return 1000

    def tear(self, node: Node) -> Any:
        factory = TearerFactory()

        # test
        test = None
        if (
            len(node.children) > 0
            and node.children[0].label == "test"
            and len(node.children[0].children) > 0
        ):
            ast_item = ast.parse(node.children[0].children[0].label)
            test = ast_item.body[0].value

        # body
        body = []
        if (
            len(node.children) > 1
            and node.children[1].label == "body"
            and len(node.children[1].children) > 0
        ):
            body_node = node.children[1]
            for child in body_node.children:
                if child.label in ["If", "While", "For"]:
                    tearer = factory.get_tearer(child)
                    item = tearer.tear(child)
                else:
                    ast_item = ast.parse(child.label)
                    item = ast_item.body[0]
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
                if child.label in ["If", "While"]:
                    tearer = factory.get_tearer(child)
                    item = tearer.tear(child)
                else:
                    ast_item = ast.parse(child.label)
                    item = ast_item.body[0]
                orelse.append(item)

        return (
            If(test=test, body=body, orelse=orelse, lineno=None)
            if node.label == "If"
            else While(test=test, body=body, orelse=orelse, lineno=None)
        )
