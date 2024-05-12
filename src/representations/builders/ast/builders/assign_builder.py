from representations.builders.ast.builders.base_builder import BaseBuilder
from representations.tree.node import Node


class AssignBuilder(BaseBuilder):
    def build(self, root_item):
        name = type(root_item).__name__
        node = Node(name)

        # targets
        self.build_targets(root_item, node)
        
        # op
        if hasattr(root_item, "op"):
            op_node = self.get_node(root_item.op)
            node.add_child(op_node, "op")
        
        # value
        self.build_value(root_item, node)

        return node
    
    def is_match(self, item):
        name = type(item).__name__
        return name in ["Assign", "AugAssign"]
