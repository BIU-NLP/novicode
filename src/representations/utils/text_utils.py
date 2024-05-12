from functools import reduce
import re
import yaml
import os
from pathlib import Path

yaml_file_path = os.path.join(
    Path(__file__).parent, "../../config/representations/terms.yaml"
)

with open(yaml_file_path, "r") as stream:
    try:
        TERMS = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


def has_conjunction(root_node, children):
    ccomp_conjoints_children = next(
        (
            children[i].children
            for i in range(1, len(children))
            if (children[i - 1].text == "hd" and children[i].text == "ccomp")
        ),
        None,
    )
    children = (
        children if ccomp_conjoints_children is None else ccomp_conjoints_children
    )

    if len(children) == 0:
        return False

    child_hd_idx = next((i for i, n in enumerate(children) if n.text == "hd"), -1)

    value = child_hd_idx > -1
    value = value and reduce(
        lambda v, r: v or r,
        [
            (
                child_node.text in ["conj", "advcl"]
                and (
                    root_node.text not in ["trigger"]
                    or children[0].text not in ["mark"]
                )
            )
            for child_node in children
        ],
    )
    value = value or reduce(
        lambda v, r: v or r,
        [
            (
                child_node.text in ["xcomp"]
                and has_conjunction(root_node, child_node.children)
            )
            for child_node in children
        ],
    )
    value = value and (root_node.text != "trigger" or not is_node_condition(root_node))
    return value


def has_condition(node):
    if node is None:
        return False

    value = reduce(
        lambda v, r: v or r,
        [is_node_condition(child_node) for child_node in node.children],
        False,
    )
    return value


def has_condition_nested_action(node):
    if node is None:
        return False

    value = reduce(
        lambda v, r: v or r,
        [is_node_condition_nested_action(child_node) for child_node in node.children],
        False,
    )
    return value


def has_condition_else(node):
    if node is None:
        return False

    value = reduce(
        lambda v, r: v or r,
        [is_node_condition_else(child_node) for child_node in node.children],
        False,
    )
    return value


def is_node_conjunction(node):
    root_node = node.parent
    children = root_node.children
    value = (
        node.text in ["conj", "advcl"]
        and (root_node.text not in ["trigger"] or children[0].text not in ["mark"])
    ) and not is_node_condition(node)
    value = value or (
        node.text in ["xcomp"] and has_conjunction(root_node, node.children)
    )
    value = value or (
        node.text in ["advmod"] and node.get_label().lower().startswith("as soon as")
    )
    value = value and (root_node.text != "trigger" or not is_node_condition(root_node))
    return value


def is_node_condition_simple(node):
    if node is None:
        return False

    """
    advcl: if ...
    obl: in the event that ... 
    csub: having that ...
    """
    value = node.text in ["advcl", "obl", "csubj"] and is_node_condition(node)
    return value


def is_node_condition_nested_action(node):
    if node is None or node.parent is None:
        return False

    parent_node = node.parent
    current_index = parent_node.children.index(node)
    previous_node = (
        parent_node.children[current_index - 1] if current_index > 0 else None
    )
    previous_node = (
        previous_node.children[-1]
        if previous_node and previous_node.text == "trigger"
        else previous_node
    )
    next_node = (
        parent_node.children[current_index + 1]
        if current_index < (len(parent_node.children) - 1)
        else None
    )
    value = is_node_condition(node.parent) and (
        (node.text == "hd" and current_index == 0)
        or (node.text in ["ccomp", "obj"] and current_index == 1)
    )
    value = value and (
        (next_node and node.text == "hd" and next_node.text in ["ccomp", "obj"])
        or (
            previous_node
            and previous_node.text == "hd"
            and node.text in ["ccomp", "obj"]
        )
    )
    return value


def is_node_condition(node, terms=None):
    """ """
    if node is None:
        return False

    terms = terms or TERMS["conditions"]

    value = reduce(
        lambda v, r: v or r,
        [node.get_label().lower().startswith(t.lower()) for t in terms],
    )
    return value


def is_node_condition_else(node, terms=None):
    if node is None:
        return False

    terms = terms or TERMS["else"]

    value = node.text in ["conj", "advcl", "parataxis", "xcomp"] and reduce(
        lambda v, r: bool(v) or bool(r),
        [
            re.match(rf"(?i)^(.*?(\b{t}\b)[^$]*)$", node.get_label().lower())
            for t in terms
        ],
    )
    return value
