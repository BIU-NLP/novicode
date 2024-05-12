from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class ForTearer(BaseTearer):
    def is_match(self, node):
        return node.label == "For"

    def tear(self, node: Node) -> Any:
        factory = TearerFactory()

        # test
        iter = None
        target = None
        if len(node.children) > 0 and node.children[0].label == "test":
            test_node = node.children[0]
            # iter
            iter_node = test_node.children[0]
            iter = (
                factory.get_tearer(iter_node.children[0]).tear(iter_node.children[0])
                if iter_node.children
                else None
            )

            # target
            target = (
                factory.get_tearer(test_node.children[1]).tear(test_node.children[1])
                if test_node.children
                else None
            )

        # body
        body = []
        body_node = node.children[1]
        for child in body_node.children:
            tearer = factory.get_tearer(child)
            item = tearer.tear(child)
            body.append(item)

        return For(body=body, iter=iter, target=target, lineno=None)
