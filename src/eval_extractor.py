from typing import List
import argparse
import glob
import os
from pathlib import Path
import pandas as pd
import numpy as np
from enum import Enum
import re
from main_representations import (
    generate_code_representation,
    generate_text_representation,
)
from utils.utils import (
    printProgressBar,
)


class States(Enum):
    IMPORTS = "imports"
    METHOD = "method"
    DOCSTRING = "docstring"
    TEST = "test"
    CODE = "code"


def get_input_file_paths(input_file_path_regexp: str):
    """
    Get input file paths.

    params:
    input_file_path_regexp: str. Regular expression for input file paths.

    returns:
    input_file_paths: list. List of input file paths.
    """
    input_file_paths = glob.glob(input_file_path_regexp)
    input_file_paths = sorted(input_file_paths)
    return input_file_paths


def read_test_file(
    input_file_path: str,
    docstring_prefix: str = '"""',
    docstring_suffix: str = '"""',
    id_prefix: str = "def test_",
    id_suffix: str = "():\n",
    code_block_start_str: str = "# start code block to test",
    code_block_end_str: str = "# end code block to test",
    compact: bool = False,
):
    """
    Read data from input file and parse it into a list of id, text and code dictionaries.
    The text and code values are enclosed in python function definitions.
    Text is expcted to be enclosed in triple quotes docstrings. A test is expected to
    follow the docstring.

    params:
    input_file_path: str. Input file path.

    returns:
    A list of id, text and test dictionaries.
    """
    with open(input_file_path, "r") as f:
        data = []
        id = None
        imports = None
        text = None
        code = None
        test = None
        leading_spaces = 0

        state = None
        lines = f.readlines()
        for i, line in enumerate(lines):
            if state in [States.DOCSTRING, States.TEST, States.CODE] and (
                len(lines) == i + 1 or lines[i + 1].startswith(id_prefix)
            ):
                item = {
                    "test_id": test_id,
                    "sample_id": sample_id,
                    "sample_minor_id": sample_minor_id,
                    "text": text,
                    "code": code,
                    "test": test,
                    "imports": imports,
                }
                data.append(item)

                text = None
                test = None
                code = None

            elif line.startswith(id_prefix):
                test_id = str(line[len(id_prefix) : -len(id_suffix)].strip())
                sample_id = test_id.split("_")[0]
                sample_minor_id = (
                    test_id.split("_")[1] if len(test_id.split("_")) > 1 else None
                )
                # if text and test:
                #     item = next(
                #         (
                #             item
                #             for item in data
                #             if sample_id and sample_id == item.get("sample_id")
                #         ),
                #         None,
                #     )
                #     if not compact or not item:
                #         item = {
                #             "test_id": test_id,
                #             "sample_id": sample_id,
                #             "sample_minor_id": sample_minor_id,
                #             "text": text,
                #             "code": code,
                #             "test": test,
                #             "imports": imports,
                #         }
                #         data.append(item)
                #     else:
                #         item[
                #             f"test_{str(line[len(id_prefix) : -len(id_suffix)].strip().split('_')[1])}"
                #         ] = test

                leading_spaces = len(line) - len(line.lstrip()) + 4
                state = States.METHOD

            elif state == States.METHOD:
                if line.strip().startswith(docstring_prefix):
                    state = States.DOCSTRING  # start code block to test

            elif state == States.DOCSTRING:
                if line.strip().startswith(docstring_suffix):
                    state = States.TEST
                else:
                    text = line.strip() if text is None else f"{text} {line.strip()}"

            elif state == States.TEST:
                if line.strip().startswith(code_block_start_str):
                    state = States.CODE
                test = add_line_to_var(test, line, leading_spaces=leading_spaces)

            elif state == States.CODE:
                if line.strip().startswith(code_block_end_str):
                    state = States.TEST
                    test = add_line_to_var(test, line, leading_spaces=leading_spaces)
                else:
                    code = add_line_to_var(code, line, leading_spaces=leading_spaces)

            if state == States.IMPORTS or line.strip().startswith("import") or line.strip().startswith("from"):
                state = States.IMPORTS
                imports = add_line_to_var(imports, line, leading_spaces=leading_spaces)

        return data


def add_line_to_var(var, line, leading_spaces=0):
    if var is None:
        var = line[leading_spaces:]
    else:
        var += line[leading_spaces:] if line.strip() != "" else line
    return var


def write_data(data: List, output_file: str):
    df = pd.DataFrame(data)
    df = df.replace(np.nan, "", regex=True)  # Replace NaN with empty string
    base_path = os.path.dirname(os.path.abspath(output_file))  # Get base path
    Path(base_path).mkdir(
        parents=True, exist_ok=True
    )  # Create directory if it doesn't exist
    compression = "gzip" if Path(output_file).suffix == ".gz" else None
    df.to_csv(
        output_file, index=False, header=True, compression=compression
    )  # Write data to file
    print(f'Generated {len(data)} test cases in "{output_file}"')


def main(
    input_file_path_regexp: str,
    output_file: str,
    lang_representations: bool = True,
    code_representations: bool = True,
    compact: bool = False,
):
    """
    Main function.

    params:
    input_file_path_regexp: str. Regular expression for input file paths.
    output_file: str. Output file path.
    """
    test_file_paths = get_input_file_paths(input_file_path_regexp)

    test_data = []
    for input_file_path in test_file_paths:
        test_data += read_test_file(input_file_path, compact=compact)

    for i, row in enumerate(test_data):
        text = row["text"]
        code = row["code"]

        if text:
            if lang_representations:
                lang_rep_raw_tree, lang_rep_tree = generate_text_representation(text, rules_enabled=True)
                lang_rep = str(lang_rep_tree if lang_rep_tree is not None else "")
                lang_rep_raw = str(lang_rep_raw_tree if lang_rep_raw_tree is not None else "")
            else:
                lang_rep = row["lang_rep"]
                lang_rep_raw = row["lang_rep_raw"]
                
            for (key, value) in [("lang_rep", lang_rep), ("lang_rep_raw", lang_rep_raw)]:
                row[key] = re.sub(
                    rf"\s+", " ", value
                ).strip()  # replace multiple spaces, \n and \t with a space
        else:
            row["lang_rep"] = None
            row["lang_rep_raw"] = None

        if code:
            if code_representations:
                code_rep_raw_tree, code_rep_tree = generate_code_representation(code, rules_enabled=True)
                code_rep = str(code_rep_tree if code_rep_tree is not None else "")
                code_rep_raw = str(code_rep_raw_tree if code_rep_raw_tree is not None else "")
            else:
                code_rep = row["code_rep"] if "code_rep" in row else ""
                code_rep_raw = row["code_rep_raw"] if "code_rep_raw" in row else ""
                
            for (key, value) in [("code_rep", code_rep), ("code_rep_raw", code_rep_raw)]:
                row[key] = re.sub(
                    rf"\s+", " ", value
                ).strip()  # replace multiple spaces, \n and \t with a space
        else:
            row["code_rep"] = None
            row["code_rep_raw"] = None

        printProgressBar(
            i + 1, len(test_data), prefix="Progress:", suffix="Updated", length=50
        )

    write_data(test_data, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="API Files Ingestor")
    parser.add_argument("--lang_representations", default=True, action="store_true")
    parser.add_argument("--code_representations", default=True, action="store_true")
    parser.add_argument("--compact", default=False, action="store_true")
    parser.add_argument(
        "--input_file_path_regexp", type=str, help="Input file path regexp"
    )
    parser.add_argument("--output_file", type=str, help="Output file path")

    main(**vars(parser.parse_args()))
