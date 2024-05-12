from representations.builders.base_tree_builder import BaseTreeBuilder
from representations.builders.lang.parsers.factory import create_parser
from representations.tree.node import Node
from representations.tree.tree import Tree


class TextTreeBuilder(BaseTreeBuilder):
    def __init__(
        self,
        parser=None,
        parser_name="stanza",
    ) -> None:
        super().__init__()
        self.parser = parser or create_parser(parser_name)

    def build(self, input) -> Tree:
        docs = self.parser.parse(input)

        tree = Tree(input=input)
        for i, doc in enumerate(docs):
            root = self.parser.get_root(doc)
            root_node = self._build_tree(root, doc)
            if i == 0:
                tree.root_node = root_node
            else:
                tree.extra_root_nodes.append(root_node)

        return tree

    def _build_tree(self, token, doc) -> Node:
        id, label, dep, head, root, terminal = self.parser.get_token_info(token, doc)
        # create the dependency node for the token
        dep_node = Node(id=id, label=dep, dep=True, head=head, root=root)
        # get all the children of the token
        children = self.parser.get_token_children(token, doc)
        # recursively build the tree
        for child, child_is_head in children:
            if child_is_head:
                # if the child is the head token, create a new node for the head
                child_node = Node(id=id, label=label, terminal=terminal)
                if len(children) > 1:
                    # if the token has more than one child, create a new node for the head and add the child to that node
                    head_node = Node(id=id, head=True)
                    head_node.add_child(child_node)
                    dep_node.add_child(head_node)
                else:
                    # if the token has only one child, add the child to the dependency node
                    dep_node.add_child(child_node)
            else:
                # if the child is not the head token, recursively build the child tree and add that tree to the current node
                child_node = self._build_tree(child, doc)
                dep_node.add_child(child_node)

        return dep_node
