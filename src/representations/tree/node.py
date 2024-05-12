from __future__ import annotations
import re
from typing import List, Optional
import uuid
import itertools

INDENT = "\t"


class Node:
    def __init__(
        self,
        label=None,
        id=None,
        parent=None,
        children=[],
        dep=False,
        head=False,
        root=False,
        terminal=False,
    ) -> None:
        self.id = id or uuid.uuid4().hex
        self.parent = parent
        self.dep = dep
        self.head = head
        self.root = root
        self.terminal = terminal
        self.edges = {}

        self.children = []
        if children:
            self.set_children(children)

        if root:
            label = "root"
        elif head:
            label = "hd"
        else:
            label = label

        self.label = label
        self.orig_label = self.label

    def __repr__(self) -> str:
        depth = self.get_depth()
        if len(self.children) == 0:
            label = f"{INDENT * depth}[ {self.label} ]\n"
        else:
            label = f"{INDENT * depth}[ {self.label} \n"
            if len(self.children) > 0:
                label += f"{''.join([str(child) for child in self.children])}"
            label += f"{INDENT * depth}]\n"
        return label

    def __str__(self) -> str:
        depth = self.get_depth()
        if len(self.children) == 0:
            label = f"{INDENT * depth}[ {self.label if self.label not in [','] else f'{{{self.label}}}'} ]\n"
        else:
            label = f"{INDENT * depth}[ {self.label}\n"
            if len(self.children) > 0:
                label += f"{''.join([str(child) for child in self.children])}"
            label += f"{INDENT * depth}]\n"
        return label

    def add_child(self, node, edge_label: str = None) -> None:
        previous_parent = node.parent
        node.parent = self
        self.children.append(node)
        if previous_parent:
            previous_parent.children = [
                child_node
                for child_node in previous_parent.children
                if child_node.id != node.id
            ]

        if edge_label:
            self.edges[(self, node)] = edge_label

    def detach(self) -> None:
        previous_parent = self.parent
        self.parent = None
        if previous_parent:
            previous_parent.children = [
                child_node
                for child_node in previous_parent.children
                if child_node.id != self.id
            ]

    def get_depth(self) -> int:
        if self.label == "root" and len(self.children) > 0:
            depth = 0
        elif self.parent is None:
            depth = 1
        else:
            depth = 1 + self.parent.get_depth()

        return depth

    def get_children(
        self,
        label=None,
        text=None,
        parent=None,
        siblings=None,
        children=None,
        head=False,
        direct=False,
        skip=None,
    ) -> Optional[List[Node]]:
        """Get child node of input label, if it exists, else return None"""
        children_nodes = []
        for child_node in self.children:
            if child_node.match(
                label=label,
                text=text,
                parent=parent,
                siblings=siblings,
                children=children,
                head=head,
                skip=skip,
            ):
                children_nodes += [child_node]  # found child node of input label
            elif not direct:
                grandsons_nodes = child_node.get_children(
                    label=label,
                    text=text,
                    parent=parent,
                    siblings=siblings,
                    children=children,
                    head=head,
                    direct=direct,
                    skip=skip,
                )
                if grandsons_nodes:
                    children_nodes += (
                        grandsons_nodes  # found grandson node of input label
                    )
        return children_nodes or None

    def get_label(self) -> str:
        label = ""
        for child in self.children:
            label = f"{label} {child.label if len(child.children) == 0 else child.get_label()}"
        label = re.sub(r"\s+", " ", label)
        label = label.strip()
        return label

    def get_parent(
        self,
        label=None,
        text=None,
        parent=None,
        root=False,
        siblings=None,
        direct=False,
        order=0,
    ) -> Optional[Node]:
        """Get parent node of input label, if it exists, else return None"""
        if self.parent is None:
            return None
        elif self.parent.match(
            label=label, text=text, parent=parent, root=root, siblings=siblings
        ):
            if order == 0:
                return self.parent
            else:
                order -= 1
                return self.parent.get_parent(
                    label=label,
                    text=text,
                    root=root,
                    parent=parent,
                    siblings=siblings,
                    order=order,
                )
        elif not direct:
            return self.parent.get_parent(
                label=label,
                text=text,
                parent=parent,
                root=root,
                siblings=siblings,
                order=order,
            )
        return None

    def get_root(self) -> Node:
        return self.get_parent(root=True)

    def get_siblings(
        self,
        label=None,
        text=None,
        children=None,
        parent=None,
        head=False,
        node=True,
        left: Optional[int] = None,
        right: Optional[int] = None,
        skip=None,
    ) -> Optional[List[Node]]:  # TODO: node!
        """
        Get sibling node of input label, if it exists, else return None
        In case child param is passed to this method, the node flag indicates this method to
        return the sibling node itself in addition to the children nodes
        """
        if self.root:
            return None  # root has no siblings

        if parent:
            parent_node = self.get_parent(siblings=[parent])
            return parent_node and parent_node.get_siblings(**parent[0])

        siblings = []
        index_in_parent = self.parent.children.index(self)
        for i, sibling_node in enumerate(self.parent.children):
            if i == index_in_parent:
                continue  # skip myself as a sibling

            if right is not None and i < index_in_parent:
                continue

            if left is not None and i > index_in_parent:
                continue

            match_sibling = sibling_node.match(
                label=label, text=text, children=children, head=head, skip=skip
            )
            test_left = (left in [None, 0]) or (
                left not in [None, 0] and index_in_parent - left == i
            )
            test_right = (right in [None, 0]) or (
                right not in [None, 0] and index_in_parent + right == i
            )
            if match_sibling and test_left and test_right:
                if node or not children:
                    siblings.append(sibling_node)  # found sibling node of input label
                if children:
                    # child_siblings = sibling_node.get_children(**child)  # found sibling
                    child_siblings = list(
                        itertools.chain.from_iterable(
                            filter(
                                None,
                                [node.get_children(**child) for child in children],
                            )
                        )
                    )  # find sibling's children
                    if child_siblings:
                        siblings += child_siblings
        return (
            siblings if len(siblings) > 0 else None
        )  # return None if no siblings found

    def get_text(self, remove_panctuations=True) -> str:
        text = ""
        for child in self.children:
            child_text = child.label if len(child.children) == 0 else child.get_text()
            child_space = " " if child.parent.label not in ["punct"] else ""
            text = f"{text}{child_space}{child_text}"

        text = re.sub(r"\s+", " ", text)

        if remove_panctuations:
            text = re.sub(r"[^\w\s]", "", text)

        text = text.strip()
        return text

    def has_child(
        self,
        label=None,
        text=None,
        parent=None,
        siblings=None,
        children=None,
        head=False,
        direct=False,
        skip=None,
    ) -> bool:
        """Check if current node has child of input label"""
        result = bool(
            self.get_children(
                label=label,
                text=text,
                parent=parent,
                siblings=siblings,
                children=children,
                head=head,
                direct=direct,
                skip=skip,
            )
        )
        return result

    def has_parent(
        self, label=None, parent=None, root=False, direct=False, order=0
    ) -> bool:
        """Check if current node has parent of input label"""
        parent = self.get_parent(
            label=label, parent=parent, root=root, direct=direct, order=order
        )
        return bool(parent)

    def has_siblings(
        self,
        label=None,
        text=None,
        children=None,
        parent=None,
        head=False,
        left: Optional[int] = None,
        right: Optional[int] = None,
        skip=None,
    ) -> bool:
        """Check if current node has sibling of input label"""
        sibling = self.get_siblings(
            label=label,
            text=text,
            children=children,
            parent=parent,
            head=head,
            left=left,
            right=right,
            skip=skip,
        )
        return bool(sibling)

    def insert_child(self, index, node) -> None:
        """Insert child node at input index"""
        previous_parent = node.parent
        node.parent = self
        self.children.insert(index, node)
        if previous_parent:
            previous_parent.children = [
                child_node
                for child_node in previous_parent.children
                if child_node.id != node.id
            ]

    def is_skipped(
        self,
        label=None,
        text=None,
        head=False,
        root=False,
        parent=None,
        children=None,
        siblings=None,
    ):
        """Check if the node should be skipped"""
        skip = self.match(
            label=label,
            text=text,
            head=head,
            root=root,
            parent=parent,
            children=children,
            siblings=siblings,
        )
        return skip

    def match(
        self,
        label=None,
        text=None,
        head=False,
        root=False,
        parent=None,
        siblings=None,
        children=None,
        index=None,
        skip=None,
    ) -> bool:
        """Check if current node matches input label, head, root, and child"""
        # result = not (
        #     bool(skip) and any([self.is_skipped(**skip_options) for skip_options in skip])
        # )
        result = not (
            skip and any([self.is_skipped(**skip_options) for skip_options in skip])
        )

        if label:
            result = (
                result
                and (
                    (
                        isinstance(label, str)
                        and isinstance(self.label, str)
                        and bool(re.search(rf"^{label}$", self.label))
                    )
                    or (
                        isinstance(label, list)
                        and any([bool(re.search(rf"^{l}$", self.label)) for l in label])
                    )
                )
                and not self.terminal
            )
        elif root:
            result = result and self.root
        elif head:
            result = result and self.head

        if text:
            result = result and (
                (
                    isinstance(text, str)
                    and bool(re.search(text, self.get_text(), re.IGNORECASE))
                )
                or (
                    isinstance(text, list)
                    and any(
                        [
                            bool(re.search(t, self.get_text(), re.IGNORECASE))
                            for t in text
                        ]
                    )
                )
            )  # self.get_text() == text

        if parent:
            result = result and self.has_parent(**parent)

        if siblings:
            result = result and any(
                [self.has_siblings(**sibling) for sibling in siblings]
            )

        if children:
            result = result and any([self.has_child(**child) for child in children])

        if index:
            node_index = self.parent.children.index(self)
            result = result and index == node_index

        return result

    def set_children(self, children) -> None:
        """Set children of current node"""
        self.children = []
        for child_node in children:
            self.add_child(child_node)

    def rename(self, label=None, parent=False, sibling=False, label_postfix=None):
        new_label = self.label
        if label:
            new_label = label
        elif parent:
            new_label = self.parent.label
        elif sibling:
            new_label = self.parent.children[self.parent.children.index(self) - 1].label

        if label_postfix and not new_label.endswith(label_postfix):
            new_label = f"{new_label}{label_postfix}"
        self.update(label=new_label)

    def replace_with(self, node) -> None:
        """Replace current node with input node"""
        parent = self.parent
        index = parent.children.index(self)
        parent.insert_child(index, node)
        children = self.children
        node.set_children(children)
        self.detach()

    def starts_with(self, value: str, remove_panctuations: bool = True) -> bool:
        text = self.get_text()
        result = text.startswith(value, remove_panctuations=remove_panctuations)
        return result

    @classmethod
    def unparse(cls, text: str) -> Node:
        """Parse text into a node tree"""
        text = re.sub(
            r"\s+", " ", text
        )  # replace all new lines and spaces with a single space
        text = text.strip()

        if text.startswith("[") and text.endswith("]"):
            text = text[1:-1].strip()

        if text.startswith("[") and text.endswith(
            "]"
        ):  # if text shows a string representation of a list (e.g. [1,2,3])
            node = Node(label=text)
            return node

        items = text.split("[ ", 1)
        label = items[0].strip()
        node = Node(label=label, head=(label == "hd"), root=(label == "root"))

        if len(items) == 1:
            return node

        tokens = f"[ {items[1]}".strip().split(" ")
        child = []
        count = 0
        for token in tokens:
            child.append(token)
            if token.startswith("[") and token != '[]':
                count += 1
            elif token.endswith("]") and token != '[]':
                count -= 1
                if count == 0:
                    child_text = " ".join(child)
                    child_node = cls.unparse(child_text)
                    node.add_child(child_node)
                    child = []

        return node

    def update(self, label=None, head=None, root=None, children=None, parent=None):
        """Update node attributes"""
        self.label = label or self.label
        self.head = head if head is not None else self.head
        self.root = root if root is not None else self.root
        if parent:
            self.detach()
            self.parent = parent
        if children:
            self.set_children(children)

    def __repr__(self):
        return self.label
