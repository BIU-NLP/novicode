from typing import Any
import importlib
from ast import *
from representations.tree.node import Node
from representations.builders.ast import tearers


class BaseTearer:
    def __init__(self, rules_enabled: bool = False) -> None:
        super().__init__()
        self.rules_enabled = rules_enabled
        
    def is_enabled(self):
        return True

    def is_match(self, node: Node) -> bool:
        raise NotImplementedError()

    def get_priority(self) -> int:
        return 100

    def tear(self, node: Node) -> Any:
        factory = tearers.tearer_factory.TearerFactory()

        class_name = node.label
        cls = getattr(importlib.import_module("ast"), class_name)

        if node.children:
            kwargs = {}
            for child_node in node.children:
                # values
                if child_node.label == "values":
                    values = []
                    for value_node in child_node.children:
                        tearer = factory.get_tearer(value_node)
                        value = tearer.tear(value_node)
                        values.append(value)
                    kwargs["values"] = values

                # value
                elif child_node.label == "value":
                    tearer = factory.get_tearer(child_node)
                    value = tearer.tear(child_node)
                    kwargs["value"] = value

                # slice
                elif child_node.label == "Slice":
                    tearer = factory.get_tearer(child_node)
                    slice = tearer.tear(child_node)
                    kwargs["slice"] = slice

            return cls(**kwargs, ctx=Load(), lineno=None)
