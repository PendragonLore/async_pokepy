from abc import ABCMeta, abstractmethod
from typing import Any


class BaseObject(metaclass=ABCMeta):
    """The abstract base class which all other full objects inherit from.

    Current list of full objects:
        * :class:`Pokemon`
        * ...

    Attributes
    ----------
    name: :class:`str`
        The object's unique name.
    id: :class:`int`
        The object's unique identifier."""
    __slots__ = ("name", "id", "_data")

    def __init__(self, data: dict):
        self._data = data

        self.id = data["id"]
        self.name = data["name"]

    def __str__(self) -> str:
        return self.name

    def __getitem__(self, item) -> Any:
        return self._data[item]

    def __eq__(self, other) -> bool:
        return isinstance(other, BaseObject) and other.id == self.id

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    @abstractmethod
    def __repr__(self) -> NotImplemented:
        return NotImplemented

    def to_dict(self) -> dict:
        """Returns the raw data of this object as a :class:`dict`.

        Returns
        -------
        :class:`dict`
            The raw data."""
        return self._data
