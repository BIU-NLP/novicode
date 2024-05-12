from representations.builders.ast.builders.base_builder import BaseBuilder
from representations.tree.node import Node


class ListBuilder(BaseBuilder):
    def build(self, root_item):
        node = super().build(root_item)

        elt_node = self.get_node(root_item.elt)
        node.add_child(elt_node, "elt")

        target_node = self.get_node(root_item.generators[0].target)
        node.add_child(target_node, "target")

        iter_node = self.get_node(root_item.generators[0].iter)
        node.add_child(iter_node, "iter")

        return node

    def is_match(self, item):
        name = type(item).__name__
        return name == "ListComp"
