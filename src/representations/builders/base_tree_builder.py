from typing import List
import copy
from representations.tree.tree import Tree
from representations.tree.node import Node
from representations.rules.node_rule import NodeRule


class BaseTreeBuilder:
    def apply_rules(self, tree: Tree, rules: List[NodeRule] = []) -> Tree:
        tree_after_rules = copy.deepcopy(tree)
        if rules:
            self.apply_rules_on_node(
                node=tree_after_rules.root_node, rules=rules, inplace=True
            )
        return tree_after_rules

    def apply_rules_on_node(
        self,
        node: Node,
        rules: List[NodeRule],
        skip: bool = None,
        inplace: bool = True,
        depth: int = 0,
    ) -> Tree:
        for rule in rules:
            rule.run_rule(node)

        children = [(c, False) for c in node.children]  # adverb, hd, obj, obl | Body
        while len([c for (c, rules_applied) in children if not rules_applied]) > 0:
            for child, rules_applied in children:
                if not rules_applied and not (
                    bool(skip)
                    and any([child.match(**skip_options) for skip_options in skip])
                ):
                    self.apply_rules_on_node(
                        node=child,
                        rules=rules,
                        skip=skip,
                        inplace=inplace,
                        depth=depth + 1,
                    )
            children = [
                (c, c in [x[0] for x in children]) for c in node.children
            ]  # 1: (adverb), (hd), Arg, Arg | 1: Test, (Body) 2: (Test), (Body)

    def build(self, input, rules_enabled=True) -> Tree:
        raise NotImplementedError()

    def tear(self, tree: Tree, rules_enabled=True) -> str:
        raise NotImplementedError()

    def _apply_rules_on_node(
        self, node, rule_configs, skip=None, inplace=True, depth=0
    ) -> Tree:
        for rule_config in rule_configs:
            rule = NodeRule(node, rule_config, self)
            rule.run_rule()

        children = [(c, False) for c in node.children]  # adverb, hd, obj, obl | Body
        while len([c for (c, rules_applied) in children if not rules_applied]) > 0:
            for child, rules_applied in children:
                if not rules_applied and not (
                    bool(skip)
                    and any([child.match(**skip_options) for skip_options in skip])
                ):
                    self._apply_rules_on_node(
                        node=child,
                        rule_configs=rule_configs,
                        skip=skip,
                        inplace=inplace,
                        depth=depth + 1,
                    )
            children = [
                (c, c in [x[0] for x in children]) for c in node.children
            ]  # 1: (adverb), (hd), Arg, Arg | 1: Test, (Body) 2: (Test), (Body)
