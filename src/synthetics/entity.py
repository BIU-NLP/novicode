from __future__ import annotations
from typing import Optional, Dict, List
import uuid
import re
from synthetics.key import Key
from synthetics.utils import (
    get_keys,
    get_labels,
    substitute_code,
    substitute_text,
    substitute_var,
)


class Entity:
    def __init__(
        self,
        key: Key,
        text: str,
        code: str,
        var: str,
        final: bool = False,
        context: Dict = {},
        **kwargs,
    ) -> None:
        self.key = key
        self.text = text
        self.template_text = text
        self.code = code
        self.template_code = code
        self.var = var
        self.text_index = None
        self.code_index = None
        self.children = []
        self.key_entity_map = {}
        self.context = context
        self.uuid = self._generate_uuid()
        self.final = final
        self.type = None
        self.syn = {}
        self.parent: Optional[Entity] = None
        self.coreference_value: Optional[str] = None
        self.coreference_entities: List[Entity] = []
        self.shown = False

        for k, v in kwargs.items():
            setattr(self, k, v)

        # if this is an indexed entity, we mark its syntax with plural number
        if len(self.key.label.split(".")) > 1:
            self.syn["num"] = "pl"

    def can_corefernce(self, entity: Entity) -> bool:
        result = (
            self.key.key == entity.key.key  # of the same key
            and entity.parent != self.parent  # do not share parent
            and self.get_coreference_text(entity) is not None  # has a coreference value
        )
        return result

    def can_corefernce_(self) -> bool:
        result = (
            self.get_coreference_value() is not None
        )  # and self.parent.get_coreference_value() is None
        return result

    def get_context_id(self) -> Optional[str]:
        context_id = self.context.get("parent", {}).get("id")
        return context_id

    def get_coreference_entity(self) -> Optional[Entity]:
        entity_type = self.get_type()
        if not entity_type:
            return

        preceding_entities = self.get_preceding_entities(entity_type=entity_type)
        coreference_entities = [e for e in preceding_entities if self.can_corefernce(e)]
        coreferenced_entity = coreference_entities[-1] if coreference_entities else None
        return coreferenced_entity

    def get_coreference_text(self, entity: Entity) -> Optional[str]:
        text = None

        coreference_value = self.get_coreference_value()
        if coreference_value and isinstance(coreference_value, str):
            return coreference_value
        elif coreference_value:
            # find the coreference values with the matching syn values
            for v in coreference_value:
                if isinstance(v, dict) and all(
                    [
                        entity.get_syn_value(k) in [None, v.get(k)]
                        for k in v.keys()
                        # if k != "value"
                    ]
                ):
                    text = v.get("value")
                    return text
                elif isinstance(v, str):
                    return v
        # else:
        #     print(f'No coreference value for entity "{self.key.label}"')

        return None

    def get_coreference_text_(self) -> Optional[str]:
        text = None
        referent_entity = (
            self.coreference_entities[-2]
            if len(self.coreference_entities) > 1
            else None
        )
        coreference_value = self.get_coreference_value()
        if referent_entity and coreference_value == f"${referent_entity.key.label}":
            text = referent_entity.get_coreference_value()
        elif coreference_value and isinstance(coreference_value, list):
            if referent_entity.key.count > 1:
                referent_entity.syn = referent_entity.syn or {}
                referent_entity.syn["num"] = "pl"
            for coref_item in coreference_value:
                result = True
                for key in [k for k in coref_item.keys() if k != "value"]:
                    referent_value = referent_entity and referent_entity.get_syn_value(
                        key
                    )
                    result = result and referent_value in [None, coref_item[key]]
                if result:
                    text = coref_item.get("value")
                    break
        else:
            text = coreference_value
        return text

    def get_coreference_value(self) -> Optional[List]:
        values = None
        if self.coreference_value:
            values = (
                self.coreference_value
                if isinstance(self.coreference_value, list)
                else [self.coreference_value]
            )
        elif self.key_entity_map and len(self.key_entity_map.values()) == 1:
            childs_of_same_type = [
                child
                for child in self.key_entity_map.values()
                if self.get_type() is not None and self.get_type() == child.get_type()
            ]
            if any(childs_of_same_type):
                child = next(iter(childs_of_same_type))
                values = child.get_coreference_value()
                values = (
                    [
                        coref_val
                        for coref_val in values
                        if not self.syn
                        or isinstance(self.syn, str)
                        or all(
                            [coref_val.get(k, v) == v for (k, v) in self.syn.items()]
                        )
                    ]
                    if values
                    else None
                )

        return values

    def get_keys(self) -> List[Key]:
        keys = get_keys(
            value=f"<text>{self.text}</text><code>{self.code}</code>",
            index=self.key.index,
        )
        return keys

    def get_labels(self) -> List[str]:
        labels = [key.label for key in self.get_keys()]
        return labels

    def get_preceding_entities(
        self, entity: Optional[Entity] = None, entity_type: Optional[str] = None
    ) -> List[Entity]:
        """
        Returns the preceding entities of the given entity and type
        """
        # only relevant for entities with text index
        if entity and entity.text_index is None:
            return []
        elif not self.parent:
            return []
        elif self.text_index is None:
            return []

        preceding_entities = []

        # preceding entities to the the parent are also preceding
        preceding_entities += self.parent.get_preceding_entities(
            entity=entity, entity_type=entity_type
        )

        # all the preceding siblings
        siblings = list(self.parent.key_entity_map.values()) if self.parent else []
        preceding_siblings = [
            s
            for s in siblings
            if s.text_index is not None and s.text_index < self.text_index
        ]

        for s in preceding_siblings:
            # any of the preceding siblings that is the given entity or has the given type
            if ((entity and s == entity) or not entity) and (
                (entity_type and s.get_type() == entity_type) or not entity_type
            ):
                preceding_entities.append(s)
            else:
                # given children of entity or type are also preceding
                preceding_entities += s.get_children(
                    entity=entity, entity_type=entity_type
                )

        return preceding_entities

    def get_syn_value(self, key: str) -> Optional[str]:
        if self.syn and key in self.syn:
            return self.syn[key]
        elif self.key_entity_map and len(self.key_entity_map.values()) == 1:
            child = next(
                (e for e in self.key_entity_map.values()),
                None,
            )
            return child.get_syn_value(key) if child else None
        else:
            return None

    def get_type(self) -> Optional[str]:
        """ """
        if self.type:
            return self.type

        var_type = None
        sub_entities = list(self.key_entity_map.values())
        if len(sub_entities) == 1:
            for sub_entity in sub_entities:
                var_type = sub_entity.get_type()
                if var_type:
                    break

        return var_type

    def get_var(self):
        if self.var is not None and not self.var.startswith("$"):
            return self.var

        var = None
        for child_key in self.children:
            child = self.children[child_key]
            var = child.get_var()
            if var:
                break
        return var

    def get_var_value(self, key: Key, child: Entity) -> str:
        var_value = f"${{{key.label}:var}}"

        # if parent has var value and child does not have a var or the parent type is identical to the child type
        # then set var value to the parent var value
        if (
            self.var
            and ((child.var is None) or (self.get_type() is not None and self.get_type() == child.get_type()))
            and not self.var.startswith("$")
        ):
            var_value = self.var
        # else if child has var value then
        #   set var value to child var value
        elif child.var:
            var_value = child.var

        if key.index and not var_value.startswith("$"):
            var_value += key.index

        return var_value

    def get_children(
        self, entity: Optional[Entity] = None, entity_type: Optional[str] = None
    ) -> List[Entity]:
        results = []

        children = self.key_entity_map.values()
        if children:
            for child in children:
                if (child == entity or not entity) and (
                    child.get_type() == entity_type or not entity_type
                ):
                    results.append(child)
                else:
                    results += child.get_children(entity, entity_type)

        return results

    def has_children(
        self, entity: Optional[Entity] = None, entity_type: Optional[str] = None
    ) -> bool:
        return bool(self.get_children(entity, entity_type))

    def is_coreference_with(self, coref_entity: Entity) -> bool:
        """
        This method checks if this entity can coreference with a given entity.
        All of the following conditions should be met:
        * Another entity of the same type is present in the sentence stack
        * The candidate source entity is not in a conjunction
        * The source entity does not share the same parent as the current entity
        * No other source type is previously coreferenced
        """
        result = (
            self.get_type() == coref_entity.get_type()  # coref to the same type
            and self.key.key == coref_entity.key.key  # coref to the same key
            and self.get_coreference_value()
            is not None  # has a text value for co-referencing
            # and coref_entity.type
            # is not None  # the source is a top level - todo!!! need to find a better way
            # and self.key.count == 1  # source entity is not brought in conjunction
            and self.context.get("parent", {}).get("id")
            != coref_entity.context.get("parent", {}).get(
                "id"
            )  # entity and coref do not share the same parent
            # and v.get("coref_context_id") != context.get("parent", {}).get("id")
        )
        return result

    def map_key_entity(self, key: Key, entity: Entity):
        if key.label not in self.key_entity_map:
            self.key_entity_map[key.label] = entity
            entity.parent = self

    def to_text(self, options: Dict = dict()) -> str:
        default_options = {"print_stack": []}
        options = {**default_options, **options}

        if coreferenced_entity := self.get_coreference_entity():
            text = self.get_coreference_text(coreferenced_entity)
            return text
        # if self.get_coreference_value() and self._is_coreference_mentioned(
        #     options["print_stack"]
        # ):
        #     options["print_stack"].append(self.uuid)
        #     text = self.get_coreference_text() or ""
        #     return text

        labels = get_labels(value=self.text)
        for label in labels:
            sub_entity = self.key_entity_map[label]

            self.text = substitute_text(
                text=self.text, key=sub_entity.key, value=sub_entity.to_text(options)
            )

        # options["print_stack"].append(self.uuid)

        text = self.text
        return text

    def to_code(self, options: Dict = dict()) -> str:
        default_options = {"print_stack": []}
        options = {**default_options, **options}

        # if coreferenced_entity := self.get_coreference_entity():
        #     code = (
        #         coreferenced_entity.to_code()
        #         # if the coreference is before the code then use the coreference code
        #         if self.code_index > coreferenced_entity.code_index
        #         else "__DELETE__"
        #     )
        #     coreferenced_entity.coreference_entities.append(self)
        #     return code
        # elif self.coreference_entities:
        #     coreferred_entity = next(iter(self.coreference_entities))
        #     if self.code_index < coreferred_entity.code_index:
        #         return "__DELETE__"

        child_labels = get_labels(value=self.code, ignore_regex="\\:var$")
        for child_label in child_labels:
            child = self.key_entity_map[child_label.split(":text")[0]]

            # replace child value and var in parent with child value and var
            to_text = child_label.endswith(":text")
            if to_text:
                self.code = self.code.replace(
                    child_label, child.key.label
                )  # replace child label with child key label to facilitate value replacedment
                code_value = child.to_text(options)
            else:
                code_value = child.to_code(options)
                
                if coreferenced_entity := child.get_coreference_entity():
                    code_value = (
                        coreferenced_entity.to_code()
                        # if the coreference is before the code then use the coreference code
                        if self.code_index < coreferenced_entity.code_index
                        else "__DELETE__"
                    )
                    coreferenced_entity.coreference_entities.append(child)
                    # return code
                elif child.coreference_entities:
                    coreferred_entity = next(iter(child.coreference_entities))
                    if child.code_index < coreferred_entity.code_index:
                        code_value = "__DELETE__"

            var_value = self.get_var_value(key=child.key, child=child)

            self.var = substitute_var(
                var=self.var,
                key=child.key,
                var_value=var_value,
            )

            self.code = substitute_code(
                code=self.code,
                key=child.key,
                code_value=code_value,
                var_value=var_value,
                child_var=child.var,
            )

        options["print_stack"].append(self.uuid)

        code = self.code
        return code

    def _code_startswith(self, s: str) -> bool:
        return (
            self.code.startswith(s)
            or bool(
                self.parent
                and re.search(re.escape(f"{s}${{{self.key}}}"), self.parent.code)
            )
            or (self.parent and self.parent._code_startswith(s))
        )

    def _generate_uuid(self) -> str:
        value = self.key.key + "_" + str(uuid.uuid4()).split("-")[0]
        return value

    def _is_coreference_mentioned(self, print_stack: List[str]) -> bool:
        """
        This method checks whether any of the coreference entities in
        the coreference segment were already mentioned (and therefore
        we would probably like to list this entity by its coreference
        value)
        """
        result = any(
            [self._is_preceding(e) for e in self.coreference_entities if e != self]
        )
        return result
        # result = len(self.coreference_entities) > 0 and any(
        #     [
        #         (coref_entity.uuid in print_stack)
        #         for coref_entity in self.coreference_entities
        #         if coref_entity.uuid != self.uuid
        #     ]
        # )
        # return result

    def _is_preceding(self, e: Entity) -> bool:
        """
        This method checks whether the given entity is preceding the current entity
        """
        siblings = self.parent.children.values() if self.parent else []
        preceding_siblings = [s for s in siblings if s.index < self.index]

        if any(e in preceding_siblings):
            # if any of the preceding siblings is the given entity, then the given entity is preceding
            return True
        elif any([s.has_children(e) for s in preceding_siblings]):
            # otherwise if the given entity is the child of any of the preceding siblings', then the given entity is preceding
            return True
        elif self.parent._is_preceding(e):
            # otherwise if the given entity is preceding the parent, then the given entity is also preceding
            return True
        else:
            return False

    # def _is_top_level_coreference(self):
    #     result = self.coreference_value is not None and not (self.parent and self.get_type() == self.parent.get_type() and self.parent._is_top_level_coreference())

    def __repr__(self) -> str:
        return self.key.key
