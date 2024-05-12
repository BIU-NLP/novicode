from representations.builders.ast.builders.base_builder import BaseBuilder


class GenericBuilder(BaseBuilder):
    def build(self, root_item):
        return super().build(root_item)

    def get_priority(self):
        return 0

    def is_match(self, item):
        return True
