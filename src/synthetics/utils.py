from typing import List
import re
import uuid
from collections import Counter
from typing import List, Union, Tuple, Optional, Dict
import csv
import os
import json
from synthetics.key import Key


def get_root_entity(entity: Dict) -> Optional[Dict]:
    if entity.get("type"):
        return entity

    root_entity = None
    for arg in entity.get("children", {}).keys():
        arg = entity["children"].get(arg)
        root_entity = get_root_entity(arg)
        if root_entity:
            break

    return root_entity


def get_keys(
    value: str,
    index: Optional[str] = None,
    label_regex: str = r"\$\{([^\$]+)\}",
    params_regex: str = r"(?<=\[).+?(?=\])",
    key_function_divider: str = ":",
) -> List[Key]:
    # find all keys enclosed in ${}
    labels = get_labels(value, label_regex=label_regex)
    # labels = [label for label in labels if not label.endswith(":var")]

    key_labels = list(
        dict.fromkeys(
            [
                # label.rsplit(f"{key_function_divider}text", 1)[0].strip()
                label.rsplit(key_function_divider, 1)[0].strip()
                for label in labels
                if not key_function_divider in label
                # if not label.endswith(
                #     f"{key_function_divider}var"
                # )  # filter out var keys ${*:var}
            ]
        )
    )  # remove duplicates while preserving order

    # split indexed keys as in ${*.1} and ${*.2}...
    index_prefix = f"{index}_" if index is not None else ""
    counter = Counter([key_label.split(".")[0] for key_label in key_labels])
    keys = [
        (
            Key(
                label=key_label,
                index_prefix=index_prefix,
                count=counter[key_label.split(".")[0]],
            ),
            json.loads(re.search(params_regex, key_label).group(0).replace("'", '"'))
            if re.search(params_regex, key_label)
            else {},
        )
        for key_label in key_labels
    ]
    return keys


def get_labels(
    value: str, label_regex: str = r"\${([^\$]+)}", ignore_regex: Optional[str] = None
) -> List[str]:
    labels = re.findall(label_regex, value)
    labels = [
        label.strip()
        for label in labels
        if not ignore_regex or not re.search(ignore_regex, label)
    ]
    return labels


def get_code(d: dict) -> str:
    code = d["code"] if "code" in d else d["text"]
    code = str(code).strip()
    return code


def get_context_id() -> str:
    context_id = str(uuid.uuid4()).split("-")[0]
    return context_id


def get_value_context_id(context) -> Optional[str]:
    value_context_id = context.get("parent", {}).get("id")
    return value_context_id


def get_var(value: dict, context: List[str]) -> Optional[str]:
    if "var" in value and value["var"] is not None:
        var = value["var"]
    else:
        var = None

    return var


def normalize_data(
    data: Optional[Union[str, dict]],
    key: Key,
    context: Optional[Dict] = None,
    key_divider: str = ".",
    **kwargs,
):
    value = data if isinstance(data, dict) else dict()
    value["uuid"] = key.key + "_" + str(uuid.uuid4()).split("-")[0]
    value["text"] = data.get("text") if isinstance(data, dict) else data
    value["template_text"] = value.get("text")
    value["code"] = get_code(value)
    value["template_code"] = value.get("code")
    value["var"] = get_var(value, [])
    value["key"] = key
    # value["type"] = key.key_type
    value["final"] = False
    value["args"] = dict()
    if context:
        value["context"] = context
    value = {**value, **kwargs}

    return value


def substitute_text(text: str, key: Key, value: str, options: Dict = {}) -> str:
    default_options = {
        "strip": True,
    }
    options = {**default_options, **options}

    new_text = text
    if value is not None:
        escaped_key = re.escape(key.label)
        new_text = re.sub(rf"\${{{escaped_key}}}", value, new_text)

    # post processing
    if options["strip"]:
        new_text = re.sub(r"[\s]{2,}", r" ", new_text, 1)

    return new_text


def substitute_code(
    code: str,
    key: Key,
    code_value: str,
    var_value: Optional[str],
    child_var: Optional[str] = None,
    options: Dict = {},
) -> str:
    default_options = {
        "remove_redundant_rows": True,
        "strip": True,
    }
    options = {**default_options, **options}

    new_code = code

    # get indentation
    escaped_regex = re.escape(f"${{{key.label}}}")
    if re.search(rf"\n\s*{escaped_regex}", new_code):
        indent = new_code.split(f"${{{key.label}}}")[0].split("\n")[-1]
        # indent
        code_value = re.sub(rf"\n", f"\n{indent}", code_value)

    # replace child var in parent with var value
    if var_value and child_var and var_value != child_var:
        # child_var = ... with var_value = ...
        escaped_regex = re.escape(f"{child_var} =")
        code_value = re.sub(escaped_regex, f"{var_value} =", code_value)

        # {label:var} = ... with var_value = ...
        escaped_regex = re.escape(f"${{{key.key}:var}}")
        code_value = re.sub(escaped_regex, var_value, code_value)

    # replace child key with child code
    escaped_regex = re.escape(f"${{{key.label}}}")
    new_code = re.sub(escaped_regex, code_value, new_code)

    # replace child key in parent with child code
    if code_value:
        escaped_regex = re.escape(f"${{{key.label}}}")
        new_code = re.sub(escaped_regex, code_value, new_code)

    # replace child var in parent with var value
    if var_value:
        escaped_regex = re.escape(f"${{{key.label}:var}}")
        new_code = re.sub(escaped_regex, var_value, new_code)

    # post processing
    if options["remove_redundant_rows"]:
        new_code = "\n".join(
            [
                r
                for r in new_code.split("\n")
                if "=" not in r or (r.split("=")[0].strip() != r.split("=")[1].strip())
            ]
        )

    if options["strip"]:
        new_code = new_code.strip()
        new_code = "\n".join(
            [r if r != "__DELETE__" else "\n" for r in new_code.split("\n")]
        )
        new_code = re.sub(
            r"^(.*)[^\S\n\r]{2,}", r"\1 ", new_code, 1
        )  # remove double spaces in strings
        new_code = re.sub(
            r"(\".*)[^\S\n\r]+\"", r'\1"', new_code, 1
        )  # remove trailing spaces in strings enclosed in double quotes

    return new_code


def substitute_var(var: str, key: Key, var_value: Optional[str]) -> str:
    new_var = var

    if new_var and var_value:
        escaped_regex_label = re.escape(f"${{{key.label}:var}}")
        escaped_regex_key = re.escape(f"${{{key.key}:var}}")
        if re.search(escaped_regex_label, new_var):
            new_var = var_value if var == f"${{{key.label}:var}}" else new_var
        elif re.search(escaped_regex_key, new_var):
            new_var = var_value if var == f"${{{key.key}:var}}" else new_var

    return new_var


def write_csv_file(filepath, data, headers=[], delimiter=","):
    path = os.path.dirname(os.path.abspath(filepath))
    os.makedirs(path, exist_ok=True)

    with open(filepath, "wt") as fp:
        writer = csv.writer(fp, delimiter=delimiter)
        if headers:
            writer.writerow(headers)  # write header
        writer.writerows(data)
