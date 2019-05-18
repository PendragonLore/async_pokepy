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
from .abc import BaseObject
from .common import Effect, Name, VerboseEffect

__all__ = (
    "Ability",
    "AbilityEffectChange",
    "AbilityPokemon",
    "AbilityFlavorText",
)


class Ability(BaseObject):
    """Represents an ability object from the API.

    .. versionadded:: 0.1.2a

    .. container:: operations

        .. describe:: str(x)

            Returns the Pokémon's name.

        .. describe:: x[y]

            Returns a Pokémon's y attribute.

        .. describe:: x == y

            Check if two Pokémons are the same.

        .. describe:: x != y

            Check if two Pokémons are *not* the same.

    Attributes
    ----------
    id: :class:`int`
        The identifier for the ability.
    name: :class:`str`
        The name for the ability.
    is_main_series: :class:`bool`
        Whether or not the ability originated in the main series of the video games.
    generation: :class:`str`
        The name of the generation the ability originated in.
    names: List[:class:`Name`]
        The name of the ability listed in different languages.
    effect_entries: List[:class:`VerboseEffect`]
        The effect of the ability listed in different languages.
    effect_changes: List[:class:`AbilityEffectChange`]
        The list of previous effects the ability has had across version groups.
    flavor_text_entries: List[:class:`AbilityFlavorText`]
        The flavor text of the ability listed in different languages.
    pokemon: List[:class:`AbilityPokemon`]
        A list of Pokémon that could potentially have the ability."""
    __slots__ = (
        "is_main_series", "generation", "names", "effect_entries", "effect_changes", "flavor_text_entries", "pokemon"
    )

    def __init__(self, data: dict):
        super().__init__(data)

        self.is_main_series = data["is_main_series"]
        self.generation = _pretty_format(data["generation"]["name"])

        self.names = [Name(d) for d in data["names"]]
        self.effect_entries = [VerboseEffect(d) for d in data["effect_entries"]]
        self.effect_changes = [AbilityEffectChange(d) for d in data["effect_changes"]]
        self.flavor_text_entries = [AbilityFlavorText(d) for d in data["flavor_text_entries"]]
        self.pokemon = [AbilityPokemon(d) for d in data["pokemon"]]

    def __repr__(self) -> str:
        return "<Ability id={0.id} name='{0}'>".format(self)


class AbilityEffectChange:
    """Represents a past change of the effect of a move in a version group.

    .. versionadded:: 0.1.2a

    Attributes
    ----------
    effect_entries: List[:class:`Effect`]
        The previous effect of the ability listed in different languages.
    version_group: :class:`str`
        The name of the version group in which the previous effect of this ability originated."""
    __slots__ = ("effect_entries", "version_group")

    def __init__(self, data: dict):
        self.effect_entries = [Effect(d) for d in data["effect_entries"]]
        self.version_group = _pretty_format(data["version_group"]["name"])

    def __repr__(self) -> str:
        return "<AbilityEffectChange version_group='{0.version_group}'>".format(self)


class AbilityPokemon:
    """Reppresents an Pokémon of an :class:`Ability`.

    Attributes
    ----------
    is_hidden: :class:`bool`
        Whether or not this a hidden ability for the Pokémon.
    slot: :class:`int`
        The slot of the ability for the pokemon.
    pokemon: :class:`str`
        The name of the Pokémon this ability could belong to."""
    __slots__ = ("is_hidden", "slot", "pokemon")

    def __init__(self, data: dict):
        self.is_hidden = data["is_hidden"]
        self.slot = data["slot"]
        self.pokemon = _pretty_format(data["pokemon"]["name"])

    def __repr__(self) -> str:
        return "<AbilityPokemon is_hidden={0.is_hidden} slot={0.slot} pokemon='{0.pokemon}'>".format(self)


class AbilityFlavorText:
    """Represents the flavor text for a move, with a language and a version group.

    Attributes
    ----------
    flavor_text: :class:`str`
        The actual text.
    language: :class:`str`
        The name of the language in which the text is in.
    version_group: :class:`str`
        The name of the version group that uses this text."""
    __slots__ = ("flavor_text", "language", "version_group")

    def __init__(self, data: dict):
        self.flavor_text = data["flavor_text"]
        self.language = data["language"]["name"]
        self.version_group = _pretty_format(data["version_group"]["name"])

    def __str__(self) -> str:
        return self.flavor_text

    def __repr__(self) -> str:
        return "<AbilityFlavorText language='{0.language}' version_group='{0.version_group}'>".format(self)
