from __future__ import annotations
from typing import Optional
from representations.tree.node import Node


class Tree:
    def __init__(self, input, root_node: Optional[Node] = None) -> None:
        self.input = input
        self.root_node = root_node
        self.extra_root_nodes = []

    def __repr__(self) -> str:
        return self.root_node

    def __str__(self) -> str:
        return str(self.root_node)

    @classmethod
    def unparse(cls, text: str) -> Tree:
        root_node = Node.unparse(text)
        tree = Tree(input=text, root_node=root_node)
        return tree


# "[ root ]" -> [ "[", "root" ,"]" ] -> Node(root, [])
# "[ root [ S ] ]" -> [ "[", "root", "[", "S", "]", "]" ] -> Node(root, [Node(S, [])])
