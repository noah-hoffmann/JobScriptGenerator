from abc import ABC
from typing import Any


class AliasHandler(ABC):
    """Abstract class, which handles alias assignments for existing object attributes."""

    def __init__(self):
        super().__setattr__("aliases", {})

    def add_alias(self, name: str, alias: str):
        """Adds a new alias to an existing attribute.

        :param name: real/original name of the attribute
        :param alias: alternative name for the attribute
        """
        self.aliases[alias] = name

    def __getattr__(self, item: str) -> Any:
        """Tries to find the requested item by looking in the aliases dictionary.

        :param item:
        :return: the requested item
        """
        try:
            return getattr(self, self.aliases[item])
        except KeyError:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{item}'"
            )
        except AttributeError:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{item}' or '{self.aliases[item]}'"
            )

    def __setattr__(self, key: str, value: Any):
        """Sets the attribute value but resolves any aliases.

        :param key:
        :param value:
        """
        if key in self.aliases:
            super().__setattr__(self.aliases[key], value)
        else:
            super().__setattr__(key, value)

    def __delattr__(self, item):
        """Deletes the item and all its aliases.

        :param item: item to delete
        """
        real_item = self.aliases.get(item, item)
        all_aliases = [key for key, value in self.aliases.items() if value == real_item]
        for key in all_aliases:
            del self.aliases[key]
        super().__delattr__(real_item)
