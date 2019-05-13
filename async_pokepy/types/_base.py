# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2019 Lorenzo

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from abc import ABCMeta, abstractmethod
from typing import Any

from ..utils import _pretty_format


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

        self.id = data["id"]  # pylint: disable=invalid-name
        self.name = _pretty_format(data["name"])

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
