from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class AssignTearer(BaseTearer):
    def is_match(self, node):
        return node.label in ["Assign", "Assign_", "AugAssign"]

    def tear(self, node: Node) -> Any:
        factory = TearerFactory()
        if node.label in ["Assign", "Assign_"]:
            # targets
            targets = (
                [
                    factory.get_tearer(child).tear(child)
                    for child in node.get_children(label="Name", direct=True)
                ]
                if not node.label.endswith(
                    "_"
                )  # check that the node label is "Assign" and not "Assign_"
                else [
                    factory.get_tearer(node.children[0]).tear(node.children[0])
                ]  # otherwise the node label is "Assign_" and we need to get the first child
            )

            # value
            value_node = node.children[1]
            tearer = factory.get_tearer(value_node)
            value = tearer.tear(value_node)

            return Assign(targets=targets, value=value, lineno=None)

        elif node.label in ["AugAssign", "AugAssign_"]:
            # target
            target = (
                self.tear_name(node.children[0])
                if not self.label.endswith("_")
                else self.tear_name(node.children[0])
            )

            # op
            op = self.tear_op(node.children[1])

            # value
            value = factory.get_tearer(node.children[2]).tear(node.children[1])

            return AugAssign(target=target, op=op, value=value, lineno=None)

    def tear_op(self, node: Node) -> Any:
        if node.label == "Add":
            return Add()
        elif node.label == "Sub":
            return Sub()
        elif node.label == "Mult":
            return Mult()
        elif node.label == "Div":
            return Div()
        else:
            return None
