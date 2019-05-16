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

from ..utils import _pretty_format

__all__ = (
    "Name",
    "VerboseEffect",
    "VersionGameIndex",
)


class Name:
    """Represents a name associated with a language.

    .. versionadded:: 0.1.0a

    .. container:: operations

        .. describe:: str(x)

            Returns the name.

    Attributes
    ----------
    name: :class:`str`
        The name.
    language: :class:`str`
        The language in which the name is in."""
    __slots__ = ("name", "language")

    def __init__(self, data: dict):
        self.name = _pretty_format(data["name"])
        self.language = data["language"]["name"]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "<Name name='{0.name}' language='{0.language}'>".format(self)


class VerboseEffect:
    """Represents a short and long effect entry associated with a language.

    .. versionadded:: 0.1.0a

    Attributes
    ----------
    effect: :class:`str`
        The localized effect text for in the specific language.
    short_effect: :class:`str`
        The localized effect text in brief.
    language: :class:`str`
        The language the effect is in."""
    __slots__ = ("effect", "short_effect", "language")

    def __init__(self, data: dict):
        self.effect = data["effect"]
        self.short_effect = data["short_effect"]
        self.language = data["language"]["name"]

    def __repr__(self) -> str:
        return "<VerboseEffect language='{0.language}'>".format(self)


class VersionGameIndex:
    """Represents a the version of a game index.

    Attributes
    ----------
    game_index: :class:`int`
        The internal id of a PokeAPI resource within game data.
    version: :class:`str`
        The name of the version relevant to the game index.`"""
    __slots__ = ("game_index", "version")

    def __init__(self, data: dict):
        self.game_index = data["game_index"]
        self.version = _pretty_format(data["version"]["name"])

    def __repr__(self) -> str:
        return "<VersionGameIndex game_index={0.game_index} version='{0.version}'>".format(self)
