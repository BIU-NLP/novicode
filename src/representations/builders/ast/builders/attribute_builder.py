from representations.builders.ast.builders.base_builder import BaseBuilder
from representations.tree.node import Node


class AttributeBuilder(BaseBuilder):
    def build(self, root_item):
        name = type(root_item).__name__
        node = Node(name)

        # value
        if hasattr(root_item, "value"):
            value_node = self.get_node(root_item.value)
            node.add_child(value_node, "value")

        # attr
        attr_node = Node(root_item.attr)
        node.add_child(attr_node, "attr")

        return node
    
    def is_match(self, item):
        name = type(item).__name__
        return name == "Attribute"
