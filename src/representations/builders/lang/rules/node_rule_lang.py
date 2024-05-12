from typing import List
from representations.rules.node_rule import NodeRule
from representations.tree.node import Node
from representations.tree.tree import Tree
import itertools


class NodeRuleLang(NodeRule):
    def __init__(
        self,
        node: Node,
        tree: Tree,
    ) -> None:
        self.node = node
        self.tree = tree

    def __repr__(self) -> str:
        return f"{self.node} -> {self.rule_config.get('id')}"

    def run_rule(self, log="Error") -> None:
        if not self.rule_config.get("enabled", True):
            return

        if not self.node.match(**self.rule_config.get("match", {})):
            return

        transformations = self.rule_config.get("transformations", [])

        for transformation in transformations:
            if not transformation.get("enabled", True):
                continue

            transformation.get("nest") and self.nest(
                self.node, transformation.get("nest")
            )
            transformation.get("nest_children") and self.nest_children(
                self.node, transformation.get("nest_children")
            )
            transformation.get("add_sibling") and self.add_sibling(
                self.node, transformation.get("add_sibling")
            )
            transformation.get("compact") and self.compact(
                self.node, transformation.get("compact")
            )

    def get_working_node(
        self, node=False, root=False, parent=None, child=None, sibling=None
    ) -> List[Node]:
        """Get a node from the rule"""
        if node:
            nodes = [self.node]
        elif root:
            nodes = [self.node.get_root()]
        elif parent:
            nodes = [self.node.get_parent(**parent)]
        elif child:
            nodes = self.node.get_children(**child)
        elif sibling:
            nodes = list(
                itertools.chain.from_iterable(
                    filter(
                        None,
                        [
                            self.node.get_siblings(**sibling_options)
                            for sibling_options in sibling
                        ],
                    )
                )
            )
        return nodes

    def get_action_nodes(
        self, node, current=False, root=False, parent=None, children=None, sibling=None
    ):
        if current:
            nodes = [node]
        elif root:
            nodes = [node.get_root()]
        elif parent:
            nodes = [node.get_parent(**parent)]
        elif children:
            nodes = list(
                itertools.chain.from_iterable(
                    filter(
                        None,
                        [
                            node.get_children(**child_options)
                            for child_options in children
                        ],
                    )
                )
            )
        elif sibling:
            nodes = list(
                itertools.chain.from_iterable(
                    filter(
                        None,
                        [
                            self.node.get_siblings(**sibling_options)
                            for sibling_options in sibling
                        ],
                    )
                )
            )
        else:
            nodes = [node]

        return nodes

    # rules

    def compact(self, base_node, options):
        action_nodes = self.get_action_nodes(base_node, options)
        for action_node in action_nodes:
            parent = action_node.parent
            index = parent.children.index(action_node)
            parent.insert_child(index, action_nodes.children[0])
            if options.get("rename_node"):
                parent.rename(**options.get("rename_node"))

    def nest(self, base_node, options):
        action_nodes = self.get_action_nodes(base_node, options)
        for action_node in action_nodes:
            parent = action_node.parent
            index = parent.children.index(action_node)

            node_args = options.get("node_args")
            assert node_args
            node_options = {"children": [action_node], **node_args}
            node = Node(**node_options)

            parent.insert_child(index, node)

        # print(
        #     f"[{self.rule_config.get('id', 'N/A')}] nest {action_node.label} under {node.label}"
        # )

    def nest_children(self, base_node, options):
        action_nodes = self.get_action_nodes(base_node, options)
        assert (
            len(action_nodes) == 1
        )  # make sure this method nests children under a single node

        node_args = options.get("node_args")
        assert node_args

        parent = action_nodes[0]
        children = parent.children
        node_options = {"children": children, **node_args}
        nested_node = Node(**node_options)
        parent.set_children([nested_node])

        # print(
        #     f"[{self.rule_config.get('id', 'N/A')}] nest_children {nested_node.label} to {parent.label}"
        # )

    def add_sibling(self, base_node, options):
        action_nodes = self.get_action_nodes(base_node, **options.get("node", {}))
        for action_node in action_nodes:
            parent_options = options.get("parent") or {"order": 1}
            parent = action_node.get_parent(**parent_options)
            assert parent

            index = self.get_insert_sibling_index(sibling=action_node)
            if index != -1:
                parent.insert_child(index=index, node=action_node)

            if options.get("rename_node"):
                action_node.rename(**options.get("rename_node"))

            # print(
            #     f"[{self.rule_config.get('id', 'N/A')}] add_sibling {action_node.label} to {parent.label}"
            # )

    def get_insert_sibling_index(self, sibling):
        parent = sibling.parent
        children = parent.children
        sibling_index = children.index(sibling)
        parent_index = parent.parent.children.index(parent)

        if sibling_index == 0:
            insert_index = max(parent_index, 0)
        elif sibling_index == len(children) - 1:
            insert_index = parent_index + 1
        else:
            insert_index = -1

        return insert_index
