from __future__ import annotations
from typing import Any
from abc import abstractclassmethod, abstractmethod


class Entity:
    """
    The Entity class is the base class for all entities. Entities are used to represent objects in the API.
    Any object returned by the API is an entity.
    This class is abstract and cannot be instantiated.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()
        if kwargs.get("text") is not None:
            kwargs = {**{"value": kwargs.get("text")}, **kwargs}
        self.__dict__.update(kwargs)

    @abstractmethod
    def __gt__(self, other) -> bool:
        raise NotImplementedError()

    def __str__(self) -> str:
        return getattr(self, "text")

    def __eq__(self, other: object) -> bool:
        result = type(self) == type(other)
        result = result and all(
            getattr(self, attr) == getattr(other, attr)
            if hasattr(other, attr)
            else False
            for attr in self.__dict__.keys()
            if getattr(self, attr) != None
        )
        result = result and all(
            getattr(other, attr) == getattr(self, attr)
            if hasattr(self, attr)
            else False
            for attr in other.__dict__.keys()
            if getattr(other, attr) != None
        )
        return result
