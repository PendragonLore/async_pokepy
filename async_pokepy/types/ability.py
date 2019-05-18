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
    __slots__ = ("effect_entries", "version_group")

    def __init__(self, data: dict):
        self.effect_entries = [Effect(d) for d in data["effect_entries"]]
        self.version_group = data["version_group"]["name"]

    def __repr__(self) -> str:
        return "<AbilityEffectChange version_group='{0.effect_entries}'>".format(self)


class AbilityPokemon:
    __slots__ = ("is_hidden", "slot", "pokemon")

    def __init__(self, data: dict):
        self.is_hidden = data["is_hidden"]
        self.slot = data["slot"]
        self.pokemon = data["pokemon"]["name"]

    def __repr__(self) -> str:
        return "<AbilityPokemon is_hidden={0.is_hidden} slot={0.slot} pokemon='{0.pokemon}'>".format(self)


class AbilityFlavorText:
    __slots__ = ("flavor_text", "language", "version_group")

    def __init__(self, data: dict):
        self.flavor_text = data["flavor_text"]
        self.language = data["language"]
        self.version_group = data["version_group"]

    def __str__(self) -> str:
        return self.flavor_text

    def __repr__(self) -> str:
        return "<AbilityFlavorText language='{0.language}' version_group='{0.version_group}'>".format(self)
