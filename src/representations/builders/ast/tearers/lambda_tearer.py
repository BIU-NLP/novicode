from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class LambdaTearer(BaseTearer):
    def is_match(self, node):
        return node.label == "Lambda"

    def tear(self, node: Node) -> Any:
        factory = TearerFactory()

        # args
        if (
            len(node.children) > 1
            and node.children[0].label == "args"
            and len(node.children[1].children) > 0
        ):
            args_node = node.children[1].children[0]
            tearer = factory.get_tearer(args_node)
            args = arguments(
                args=[
                    arg(arg=args_child.children[0].label, lineno=None)
                    for args_child in args_node.children
                    if args_child.label == "arg" and len(args_child.children) > 0
                ],
                vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                defaults=[],
            )
        else:
            args = None

        # body
        if (
            len(node.children) > 1
            and node.children[1].label == "body"
            and len(node.children[1].children) > 0
        ):
            body_node = node.children[1].children[0]
            tearer = factory.get_tearer(body_node)
            body = tearer.tear(body_node)
        else:
            body = None

        return Lambda(args=args, body=body, lineno=None)
