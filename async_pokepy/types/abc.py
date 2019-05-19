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

import abc
from difflib import SequenceMatcher
from typing import Any, Callable, Optional

from ..exceptions import NoMoreItems
from ..utils import _pretty_format, maybe_coroutine

__all__ = (
    "BaseObject",
    "AsyncIterator"
)


class BaseObject(metaclass=abc.ABCMeta):
    """The abstract base class which all other full objects inherit from.

    Current list of full objects:
        * :class:`Pokemon`
        * :class:`Move`
        * :class:`Ability`
        * :class:`Berry`

    .. container:: operations

        .. describe:: str(x)

            Returns the object's name.

        .. describe:: x[y]

            Returns the object's y attribute.

        .. describe:: x == y

            Check if two objects are the same.

        .. describe:: x != y

            Check if two objects are *not* the same.

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
        return isinstance(other, self.__class__) and self.id == other.id

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    @abc.abstractmethod
    def __repr__(self) -> NotImplemented:
        return NotImplemented

    def to_dict(self) -> dict:
        """Returns the raw data of the object as a :class:`dict`.

        Returns
        -------
        :class:`dict`
            The raw data."""
        return self._data


class AsyncIterator(metaclass=abc.ABCMeta):
    """Represents an abstrast asynchronous iterator.

    .. versionadded:: 0.1.0a

    .. container:: operations

        .. describe:: async for x in y

            Iterates over the contents of the async iterator."""
    __slots__ = ()

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            thing = await self.next()
        except NoMoreItems:
            raise StopAsyncIteration()
        else:
            return thing

    @abc.abstractmethod
    async def next(self) -> NotImplemented:
        """Get the next item in the iterator.

        This method **must** be implemented by a subclass.

        Raises
        ------
        NoMoreItems
            There are no more items left in the iterator.

        Returns
        -------
        :data:`~typing.Any`
            The next item from the iterator."""
        return NotImplemented

    async def flatten(self) -> list:
        """Turn the iterator in a :class:`list`.

        Returns
        -------
        :class:`list`
            The iterator's items in a list."""
        results = []

        while True:
            try:
                elem = await self.next()
            except NoMoreItems:
                return results
            else:
                results.append(elem)

    async def find(self, predicate: Callable) -> Optional[Any]:
        """Search for an id or name in the iterator.

        .. versionchanged:: 0.1.3

            The function now takes a callable as it's only parameter.

        Parameters
        ----------
        predicate: :data:`~typing.Callable`
            A function, which takes only one argument, an element of the iterator,
            that returns a boolean-like result.
            The function could be a coroutine.

        Returns
        -------
        Optional[:data:`~typing.Any`]
            The found item, could be ``None`` if it was not found."""
        while True:
            try:
                elem = await self.next()
            except NoMoreItems:
                return None

            if await maybe_coroutine(predicate, elem):
                return elem

    async def find_similar(self, name: str) -> list:
        """Does a semi-fuzzy search on the iterator.

        .. versionchanged:: 0.1.3

            The results are now sorted by similarity.

        Parameters
        ----------
        name: :class:`str`
            The name of the item.
            This might change depending of the needs of the iterator.

        Returns
        -------
        :class:`list`
            The list of similar results found, that might be empty.
            If a full match is found it will return a list with only that item.
            The list is sorted by similarity."""
        similar = []

        while True:
            try:
                elem = await self.next()
            except NoMoreItems:
                return [y[0] for y in sorted(similar, key=lambda x: x[1], reverse=True)]

            diff = int(
                round(
                    100 * SequenceMatcher(None, name.lower().strip().replace("-", " "),
                                          elem[0].replace("-", " ")).quick_ratio()
                )
            )

            if diff == 100:
                return [elem]

            if diff > 60:
                similar.append((elem, diff))
