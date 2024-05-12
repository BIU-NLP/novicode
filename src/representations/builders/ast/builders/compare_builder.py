from representations.tree.node import Node
from representations.builders.ast.builders.base_builder import BaseBuilder


class CompareBuilder(BaseBuilder):
    def build(self, root_item):
        name = type(root_item).__name__
        node = Node(name)

        if hasattr(root_item, "left"):
            left_child_node = self.get_node(root_item.left)
            node.add_child(left_child_node, "left")

        if hasattr(root_item, "ops"):
            for i, op in enumerate(root_item.ops):
                op_child_node = self.get_node(op)
                node.add_child(op_child_node, "ops")

                comparator = root_item.comparators[i]
                comparator_child_node = self.get_node(comparator)
                node.add_child(comparator_child_node, "comparators")

        return node
    
    def is_match(self, item):
        name = type(item).__name__
        return name == "Compare"
