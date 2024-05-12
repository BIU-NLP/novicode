import glob
import os
import inspect
import importlib
from representations.builders.ast.tearers.generic_tearer import GenericTearer
from representations.builders import ast


class TearerFactory:
    def get_tearer(self, item, rules_enabled=False):
        all_tearers = [Tearer(rules_enabled=rules_enabled) for Tearer in self._load_all_tearers()]
        tearers = [b for b in all_tearers if b.is_match(item) and b.is_enabled()]
        tearers = sorted(tearers, key=lambda b: b.get_priority(), reverse=True)
        tearer = next(iter(tearers), None)
        return tearer

    def _load_all_tearers(self):
        results = []
        files = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
        sub_modules = [
            os.path.basename(f)[:-3]
            for f in files
            if os.path.isfile(f) and not f.endswith("__init__.py")
        ]
        parent_module = ".".join(__name__.split(".")[:-1])
        modules = [f"{parent_module}.{sub_module}" for sub_module in sub_modules]
        for module in modules:
            for name, obj in inspect.getmembers(importlib.import_module(module)):
                if inspect.isclass(obj):
                    if (
                        issubclass(obj, ast.tearers.base_tearer.BaseTearer)
                        and obj != ast.tearers.base_tearer.BaseTearer
                    ):
                        results.append(obj)
        return results
