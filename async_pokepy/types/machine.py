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

from .abc import UnNamedBaseObject
from .common import NamedAPIObject

__all__ = ("Machine",)


class Machine(UnNamedBaseObject):
    """Represents a machine object from the API.

    .. versionadded:: 0.1.5a

    .. container:: operations

        .. describe:: str(x)

            Returns the machine item's name.

        .. describe:: x[y]

            Returns a move's y attribute.

        .. describe:: x == y

            Check if two moves are the same.

        .. describe:: x != y

            Check if two moves are *not* the same.

    Attributes
    ----------
    id: :class:`int`
        The identifier for this machine.
    item: :class:`NamedAPIObject`
        The TM or HM item that corresponds to the machine.
    move: :class:`NamedAPIObject`
        The move that is taught by the machine.
    version_group: :class:`NamedAPIObject`
        The version group that the machine applies to.
    """
    def __init__(self, data: dict):
        super().__init__(data)

        self.item = NamedAPIObject(data["item"])
        self.move = NamedAPIObject(data["move"])
        self.version_group = NamedAPIObject(data["version_group"])

    def __str__(self) -> str:
        return str(self.item)

    def __repr__(self) -> str:
        return "<Machine id={0.id} item={0.item} move={0.move}>".format(self)
