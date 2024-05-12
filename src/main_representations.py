import argparse
import pandas as pd
from typing import Optional
from representations.builders.lang.text_tree_builder import TextTreeBuilder
from representations.builders.ast.ast_tree_builder import ASTTreeBuilder
from representations.rules.node_rule import NodeRule
from representations.utils.file_utils import load_input_file, load_rules_from_file
from representations.builders.ast.tearers.tearer_factory import TearerFactory
import ast


def generate_code_representation(code: str, rules_enabled: bool = False):
    builder = ASTTreeBuilder()
    tree = builder.build(input=code, rules_enabled=False)
    # tearer = TearerFactory().get_tearer(tree.root_node, rules_enabled=False)
    # asdl = tearer.tear(tree.root_node)
    # code = ast.unparse(asdl)
    tree0 = builder.build(input=code, rules_enabled=True)

    postprocessed_tree = None
    if rules_enabled:
        postprocessed_tree = builder.apply_rules(
            tree=tree0,
        )

    return tree, postprocessed_tree


def generate_text_representation(
    text: str,
    parser_name: str = "stanza",
    rules_file_path: str = "config/representations/lang_rules.yaml",
    rules_enabled: bool = True,
):
    builder = TextTreeBuilder(parser_name=parser_name)
    tree = builder.build(input=text)

    postprocessed_tree = None
    if rules_enabled:
        rules_config = load_rules_from_file(rules_file_path)
        rules = [
            NodeRule(rule_config=rule_config)
            for rule_config in rules_config.get("rules")
        ]
        postprocessed_tree = builder.apply_rules(tree=tree, rules=rules)

    return tree, postprocessed_tree


def main(
    tree_type: str = "text",
    input: Optional[str] = None,
    input_file: Optional[str] = None,
    text_parser_name: Optional[str] = "stanza",
    show_preprocessed: bool = False,
    show_postprocessed: bool = True,
    output_file: Optional[str] = None,
) -> None:
    # populate inputs list
    inputs = []
    if input:
        inputs = [input]
    elif input_file:
        inputs = (
            pd.read_csv(input_file)
            if input_file.endswith(".csv")
            else [load_input_file(input_file)]
        )

    # build trees
    trees = []
    postprocessed_trees = []
    if tree_type == "text":
        for text in inputs:
            tree, postprocessed_tree = generate_text_representation(
                text, text_parser_name, rules_enabled=show_postprocessed
            )
            trees.append(tree)
            postprocessed_trees.append(postprocessed_tree)
    elif tree_type == "code":
        for code in inputs:
            tree, postprocessed_tree = generate_code_representation(
                code, rules_enabled=show_postprocessed
            )
            trees.append(tree)
            postprocessed_trees.append(postprocessed_tree)

    # show trees
    for i, (input, tree, postprocessed_tree) in enumerate(
        zip(inputs, trees, postprocessed_trees)
    ):
        if show_preprocessed or show_postprocessed:
            print(f"[{i+1}] Input: {input}")

        if show_preprocessed:
            print("Preprocessed tree:")
            print(tree)

        if show_postprocessed:
            print("Postprocessed tree:")
            print(postprocessed_tree)

    if output_file:
        df = pd.DataFrame(
            {"input": inputs, "tree": trees, "postprocessed_tree": postprocessed_trees}
        )
        df.save_csv(output_file, index=False, compression="gzip")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates pairs of scenario and intents"
    )
    parser.add_argument("--tree_type", type=str, default="text", help="text|code")
    parser.add_argument(
        "--input", type=str, help="sentence to parse or code to build tree"
    )
    parser.add_argument(
        "--input_file", type=str, help="path to file with sentences or code"
    )
    parser.add_argument(
        "--data_file", type=str, help="path to csv file to save the data in"
    )
    parser.add_argument(
        "--text_parser_name", type=str, default="stanza", help="stanza|spacy"
    )
    parser.add_argument(
        "--show_preprocessed", action="store_true", help="show pre processed tree"
    )
    parser.add_argument(
        "--show_postprocessed", action="store_true", help="show post processed tree"
    )
    args = parser.parse_args()

    main(
        tree_type=args.tree_type,
        input=args.input,
        input_file=args.input_file,
        text_parser_name=args.text_parser_name,
        show_preprocessed=args.show_preprocessed,
        show_postprocessed=args.show_postprocessed,
        output_file=args.data_file,
    )
