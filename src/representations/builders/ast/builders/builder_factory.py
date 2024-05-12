import glob
import os
import inspect
import importlib
from representations.builders import ast


class BuilderFactory:
    def get_builder(self, item, rules_enabled: bool = False):
        all_builders = [Builder(rules_enabled=rules_enabled) for Builder in self._load_all_builders()]
        builders = [b for b in all_builders if b.is_match(item) and b.is_enabled()]
        builders = sorted(builders, key=lambda b: b.get_priority(), reverse=True)
        builder = next(iter(builders), None)
        return builder

    def _load_all_builders(self):
        results = set()
        files = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
        sub_modules = [
            os.path.basename(f)[:-3]
            for f in files
            if os.path.isfile(f) and not f.endswith("__init__.py")
        ]
        parent_module = ".".join(__name__.split(".")[:-1])
        modules = [f"{parent_module}.{sub_module}" for sub_module in sub_modules]
        for module in modules:
            for _, obj in inspect.getmembers(importlib.import_module(module)):
                if inspect.isclass(obj):
                    if (
                        issubclass(obj, ast.builders.base_builder.BaseBuilder)
                        and obj != ast.builders.base_builder.BaseBuilder
                    ):
                        results.add(obj)
        return list(results)
