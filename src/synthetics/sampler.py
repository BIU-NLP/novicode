import re
import random
import copy
import json
import os
import glob
import yaml

from typing import Dict, Deque, List, Optional
from synthetics.key import Key
from synthetics.entity import Entity
from synthetics.utils import (
    get_keys,
    get_labels,
    normalize_data,
)
from synthetics.data_generator.faker import FakerDataGenerator


class Sampler:
    def __init__(
        self, grammar_dir: str = "config/grammar", seed: Optional[int] = None
    ):
        if seed:
            random.seed(seed)

        self.grammar = self._load_grammar(grammar_dir)

    def sample(
        self,
        key: Key = Key("utterance"),
        options: Dict = dict(),
        steps: int = 0,
        **kwargs,
    ) -> Entity:
        default_options = {"sample_children": True}
        options = {**default_options, **options}

        # sample key
        entity = self._sample_key(key=key, grammar=self.grammar, **kwargs)

        # sample sub-keys if entity can be further sampled

        text_labels = get_labels(entity.text, ignore_regex="[^\[]\:\w+")
        code_labels = get_labels(entity.code, ignore_regex="[^\[]\:\w+")

        labels = list(dict.fromkeys(text_labels + code_labels))
        for label in labels:
            if label not in entity.key_entity_map:
                sub_key = Key(label=label)
                params_regex = r"(?<=\[).+?(?=\])"
                params = (
                    json.loads(
                        re.search(params_regex, sub_key.label)
                        .group(0)
                        .replace("'", '"')
                    )
                    if re.search(params_regex, sub_key.label)
                    else {}
                )

                sub_entity = self.sample(
                    key=sub_key, steps=steps + 1, **params, **kwargs
                )
                entity.map_key_entity(sub_key, sub_entity)
            sub_entity.text_index = (
                text_labels.index(label) if label in text_labels else None
            )
            sub_entity.code_index = (
                code_labels.index(label) if label in code_labels else None
            )

        return entity

    def _get_entries_for_key(self, key: Key, data: dict) -> List[dict]:
        entries = []
        # checks if the key is in the data
        if key.key in data:
            entries = copy.deepcopy(data[key.key])
        # checks if the key is a regex in the data
        elif (
            len(
                [
                    k
                    for k in data.keys()
                    if re.search(k, key.key)  # and key.key.endswith(":text")
                ]
            )
            > 0
        ):
            k = [k for k in data.keys() if re.search(k, key.key)][0]
            entries = copy.deepcopy(data[k])
            try:
                params_str = (
                    re.search(k, key.key).group(1) if re.search(k, key.key) else None
                )
            except:
                params_str = None

            if params_str:
                for item in entries:
                    param_values = list(map(lambda x: x.strip(), params_str.split(",")))
                    params = dict()
                    # obj is a special text key in the param
                    params["obj"] = param_values[0]
                    params["obj"] = (
                        params["obj"][:-1]
                        if item.get("num") == "sg" and params["obj"].endswith("s")
                        else params["obj"]
                    )
                    # var is a special code key in the param
                    params["var"] = param_values[0]
                    # rest of the params
                    if len(param_values) > 1:
                        for param in param_values[1:]:
                            [k, v] = param.split("=")
                            params[k.strip()] = (
                                v.strip()
                                if not v.strip().startswith("{")
                                and not v.strip().endswith("}")
                                else f"${v.strip()}"
                            )
                    text_keys = get_keys(
                        value=item["text"], label_regex=r"\$([^\s\{\}}]+)"
                    )
                    for k, _ in text_keys:
                        item["text"] = re.sub(
                            re.escape(f"${k.key}"),
                            params.get(k.key, ""),
                            item["text"],
                            1,
                        )
                    code_keys = get_keys(
                        value=item["code"], label_regex=r"\$([^\s\,\(\)\{\}]+)"
                    )
                    for k, _ in code_keys:
                        item["code"] = re.sub(
                            re.escape(f"${k.key}"),
                            params.get(k.key, ""),
                            item["code"],
                            1,
                        )  # item["code"].replace(f"${k[0]}", params.get(k[0], ""))
        return entries

    def _load_grammar(self, grammar_dir: str, file_pattern: str = "**/*.yaml") -> dict:
        grammar = {}
        # load all files from grammar_dir and subdirectories
        path = os.path.join(grammar_dir, file_pattern)
        for grammar_file in glob.glob(path, recursive=True):
            with open(grammar_file, "r") as stream:
                try:
                    data = yaml.safe_load(stream)
                    if data:
                        grammar = {**grammar, **data}
                except yaml.YAMLError as exc:
                    print(exc)
        return grammar

    def _sample_coreference(
        self, coref_entity: Entity, sentence_stack: Deque[Entity]
    ) -> Optional[Entity]:
        """
        This method sample a value by key from a the sentence stack.

        If the coreference flag is switched on then try to coreference and return the source entity along with a
        corefered valued
        steps:
        1. extract the sampled value type
        2. Iterate over the sentence stack to find the most recent element with type (1)
        3. check if this value should be coreferenced
        4. If all conditions in (3) are met then
            a. Copy source entity to be the coreffed entity
            b. Update the coreffed entity to have a coreffed value
            c. Update the source entity to have a corefenced value
        """
        if not coref_entity.can_corefernce():
            return None

        source_entities = [
            entity
            for entity in sentence_stack
            if entity.is_coreference_with(coref_entity)
        ]
        source_entities_coref = source_entities[-1] if source_entities else None
        return source_entities_coref

    def _sample_from_faker(
        self, key: Key, seed: Optional[int] = None, **kwargs
    ) -> Entity:
        fake = FakerDataGenerator.get_faker(seed=seed)
        func_names = key.key.split("faker_")[1]
        result = None
        for func_name in func_names.split(" "):
            value = getattr(fake, func_name)()
            value = str(value)
            result = value if not result else f"{value} {result}"

        norm_result = normalize_data(result, key)
        entity = Entity(**norm_result)
        return entity

    def _sample_from_grammar(
        self,
        key: Key,
        grammar: Dict,
        **kwargs,
    ) -> Entity:
        data = self._sample_random_value(key=key, data=grammar)
        norm_result = normalize_data(data=data, key=key, context={}, **kwargs)
        entity = Entity(**norm_result)
        return entity

    def _sample_key(self, key: Key, grammar: Dict, **kwargs) -> Entity:
        if re.search(rf"faker_.*", key.key):
            # faker dynamic key
            entity = self._sample_from_faker(key=key, **kwargs)
        else:
            # generic dynamic key (not faker)
            entity = self._sample_from_grammar(key=key, grammar=grammar, **kwargs)

        return entity

    def _sample_random_value(
        self,
        key: Key,
        data: dict,
        k: int = 1,
        default_divider: str = "|",
    ) -> Dict:
        population = (
            self._get_entries_for_key(key, data)
            if default_divider not in key.key
            else key.key.split(default_divider)
        )
        weights = [item["weight"] if "weight" in item else 1.0 for item in population]
        results = random.choices(population, weights, k=k)
        result = results[0]
        value = copy.deepcopy(result)
        return value
