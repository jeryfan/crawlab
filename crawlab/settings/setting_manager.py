from collections.abc import MutableMapping
from copy import deepcopy
from typing import Iterator
from crawlab.settings import default_settings
from importlib import import_module


class SettingManager(MutableMapping):
    def __init__(self, values=None):
        self.attributes = {}
        self.set_settings(default_settings)
        self.update_values(values)

    def __getitem__(self, key):
        return self.attributes[key] if key in self else None

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        self.delete(key)

    def delete(self, key):
        del self[key]

    def set(self, key, value):
        self.attributes[key] = value

    def get(self, key, default=None):
        return self[key] if self[key] is not None else default

    def getint(self, key, default=0):
        return int(self.get(key, default))

    def getfloat(self, key, default=0.0):
        return float(self.get(key, default))

    def getbool(self, key, default=False):
        v = self.get(key, default)
        try:
            return bool(v)
        except ValueError:
            if v in ["False", "FALSE", "false"]:
                return False
            elif v in ["True", "TRUE", "true"]:
                return True
            else:
                raise ValueError("Only support Boolean value")

    def getlist(self, key, default=[]):
        v = self.get(key, default)
        if isinstance(v, str):
            v = v.split(",")

        return list(v)

    def set_settings(self, module):
        if isinstance(module, str):
            module = import_module(module)
        for key in dir(module):
            if key.isupper():
                self.set(key, getattr(module, key))

    def __str__(self) -> str:
        return f"<Settings values={self.attributes}>"

    __repr__ = __str__

    def __contains__(self, key):
        return key in self.attributes

    def update_values(self, values):
        if values is not None:
            for key, value in values.items():
                self.set(key, value)

    def __iter__(self) -> Iterator:
        return iter(self.attributes)

    def __len__(self) -> int:
        return len(self.attributes)

    def copy(self):
        return deepcopy(self)
