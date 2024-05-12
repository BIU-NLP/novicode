import yaml


def load_input_file(file_name):
    with open(file_name, "r") as f:
        text = f.read()
        return text


def load_rules_from_file(yaml_file_path: str):
    with open(yaml_file_path, "r") as stream:
        try:
            rules = yaml.safe_load(stream)
            return rules
        except yaml.YAMLError as exc:
            print(exc)
