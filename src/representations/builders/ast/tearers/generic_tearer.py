from typing import Any
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer


class GenericTearer(BaseTearer):
    def is_match(self, node: Node) -> bool:
        return False

    def tear(self, node: Node) -> Any:
        return super().tear(node)
