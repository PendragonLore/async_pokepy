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
    "Effect",
    "VerboseEffect",
    "VersionGameIndex",
    "APIObject",
    "NamedAPIObject",
    "MachineVersionDetail"
)


class APIObject:
    """Represents a partial API object with an ID.

    .. versionadded:: 0.1.3a

    Attributes
    ----------
    id: :class:`int`
        The object's identifier."""
    def __init__(self, data: dict):
        self.id = int(data["url"].split("/")[-2])

    def __repr__(self) -> str:
        return "<APIObject id={0.id}>".format(self)


class NamedAPIObject(APIObject):
    """Represents a partial API object with a name and ID.

    This inherits from :class:`APIObject`.

    .. versionadded:: 0.1.3a

    .. container:: operations

        .. describe:: str(x)

            Returns the object's name.

    Attributes
    ----------
    id: :class:`int`
        The object's identifier.
    name: :class:`str`
        The object's name."""
    def __init__(self, data: dict):
        super().__init__(data)

        self.name = _pretty_format(data["name"])

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "<NamedAPIObject id={0.id} name='{0}'>".format(self)


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
    language: :class:`NamedAPIObject`
        The language in which the name is in."""
    __slots__ = ("name", "language")

    def __init__(self, data: dict):
        self.name = _pretty_format(data["name"])
        self.language = NamedAPIObject(data["language"])

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "<Name language='{0.language}'>".format(self)


class VerboseEffect:
    """Represents a short and long effect entry associated with a language.

    .. versionadded:: 0.1.0a

    Attributes
    ----------
    effect: :class:`str`
        The localized effect text in the associated language.
    short_effect: :class:`str`
        The localized effect text in brief.
    language: :class:`NamedAPIObject`
        The language the effect is in."""
    __slots__ = ("effect", "short_effect", "language")

    def __init__(self, data: dict):
        self.effect = data["effect"]
        self.short_effect = data["short_effect"]
        self.language = NamedAPIObject(data["language"])

    def __repr__(self) -> str:
        return "<VerboseEffect language='{0.language}'>".format(self)


class VersionGameIndex:
    """Represents a the version of a game index.

    Attributes
    ----------
    game_index: :class:`int`
        The internal id of a PokeAPI object within game data.
    version: :class:`NamedAPIObject`
        The name of the version relevant to the game index."""
    __slots__ = ("game_index", "version")

    def __init__(self, data: dict):
        self.game_index = data["game_index"]
        self.version = NamedAPIObject(data["version"])

    def __repr__(self) -> str:
        return "<VersionGameIndex game_index={0.game_index} version='{0.version}'>".format(self)


class Effect:
    """Represents an effect description with a language.

    .. versionadded:: 0.1.2a

    .. container:: operations

        .. describe:: str(x)

            Returns the localized text.

    Attributes
    ----------
    effect: :class:`str`
        The localized effect text in the associated language.
    language: :class:`NamedAPIObject`
        The language the effect is in."""
    __slots__ = ("effect", "language")

    def __init__(self, data: dict):
        self.effect = data["effect"]
        self.language = NamedAPIObject(data["language"])

    def __str__(self) -> str:
        return self.effect

    def __repr__(self) -> str:
        return "<Effect language={0.language}>".format(self)


class MachineVersionDetail:
    """Represents the version details of a machine.

    Attributes
    ----------
    machine: :class:`APIObject`
        The machine that teaches a move from an item.
    version_group: :class:`NamedAPIObject`
        The version group of this specific machine."""
    def __init__(self, data: dict):
        self.machine = APIObject(data)
        self.version_group = NamedAPIObject(data)

    def __repr__(self) -> str:
        return "<MachineVersionDetail version_group='{0.version_group}'>".format(self)
