from abc import ABCMeta, abstractmethod
from collections.abc import MutableMapping
from typing import Any
from pprint import pformat


class Field(dict):
    pass


class ItemMeta(ABCMeta):
    def __new__(mcls, name, bases, namespace):
        field = {}
        for key, value in namespace.items():
            if isinstance(value, Field):
                field[key] = value
        instance = super().__new__(mcls, name, bases, namespace)
        instance.FIELDS = field
        return instance


class Item(MutableMapping, metaclass=ItemMeta):

    FIELDS: dict

    def __init__(self):
        self._values = {}

    def __setitem__(self, key, value):
        if key in self.FIELDS:
            self._values[key] = value
        else:
            raise KeyError("Field %s does not exist" % key)

    def __getitem__(self, key):
        return self._values[key]

    def __delitem__(self, key):
        del self._values[key]

    def __setattr__(self, key: str, value: Any) -> None:
        if not key.startswith("_"):
            raise AttributeError(
                "Field %s does not support setting value by attribute" % key
            )
        super().__setattr__(key, value)

    def __getattribute__(self, key: str) -> Any:
        fields = super().__getattribute__("FIELDS")
        if key in fields:
            raise AttributeError(
                "Field %s does not support getting value by attribute" % key
            )
        else:
            return super().__getattribute__(key)

    def __getattr__(self, key: str) -> Any:
        raise KeyError("Field %s does not exist" % key)

    def __repr__(self) -> str:
        return pformat(dict(self))

    __str__ = __repr__

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self):
        return iter(self._values)

    def to_dict(self):
        return dict(self)


if __name__ == "__main__":

    class MyItem(Item):
        name = Field()

    item = MyItem()
    item["name"] = "test"
    print(item, 333)
