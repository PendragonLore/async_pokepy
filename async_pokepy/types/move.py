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
from ._base import BaseObject
from .common import Name, VerboseEffect


class Move(BaseObject):
    __slots__ = (
        "accuracy", "effect_chance", "pp", "power_points", "priority", "power", "contest_type", "type", "target",
        "generation", "damage_class", "meta", "stat_changes", "names", "effect_entries", "flavor_text_entries",
        "past_values"
    )

    def __init__(self, data: dict):
        super().__init__(data)

        self.accuracy = data["accuracy"]
        self.effect_chance = data["effect_chance"]
        self.pp = data["pp"]
        self.power_points = self.pp
        self.priority = data["priority"]
        self.power = data["power"]

        self.contest_type = _pretty_format(data["contest_type"]["name"])
        self.type = _pretty_format(data["type"]["name"])
        self.target = _pretty_format(data["target"]["name"])
        self.generation = _pretty_format(data["generation"]["name"])
        self.damage_class = _pretty_format(data["damage_class"]["name"])

        self.meta = MoveMetaData(data["meta"])
        self.stat_changes = [MoveStatChange(d) for d in data["stat_changes"]]
        self.names = [Name(d) for d in data["names"]]
        self.effect_entries = [VerboseEffect(d) for d in data["effect_entries"]]
        self.flavor_text_entries = [MoveFlavorText(d) for d in data["flavor_text_entries"]]
        self.past_values = [PastMoveStatValues(d) for d in data["past_values"]]

    def __repr__(self) -> str:
        return "<Move id={0.id} name='{0}'>".format(self)


class MoveFlavorText:
    __slots__ = ("flavor_text", "language", "version_group")

    def __init__(self, data: dict):
        self.flavor_text = data["flavor_text"]
        self.language = data["language"]["name"]
        self.version_group = _pretty_format(data["version_group"]["name"])

    def __repr__(self) -> str:
        return "<MoveFlavorText language='{0.language}' version_group='{0.version_group}'>".format(self)


class MoveMetaData:
    __slots__ = (
        "ailment", "category", "min_hits", "max_hits", "min_turns", "max_turns", "drain", "healing", "crit_rate",
        "ailment_chance", "flinch_chance", "stat_chance"
    )

    def __init__(self, data: dict):
        self.ailment = _pretty_format(data["ailment"]["name"])
        self.category = _pretty_format(data["category"]["name"])

        self.min_hits = data["min_hits"]
        self.max_hits = data["max_hits"]
        self.min_turns = data["min_turns"]
        self.max_turns = data["max_turns"]
        self.drain = data["drain"]
        self.healing = data["healing"]
        self.crit_rate = data["crit_rate"]
        self.ailment_chance = data["ailment_chance"]
        self.flinch_chance = data["flinch_chance"]
        self.stat_chance = data["stat_chance"]

    def __repr__(self) -> str:
        return "<MoveMetaData category='{0.category}'>".format(self)


class MoveStatChange:
    __slots__ = ("change", "stat")

    def __init__(self, data: dict):
        self.change = data["change"]
        self.stat = _pretty_format(data["stat"]["name"])

    def __repr__(self) -> str:
        return "<MoveStatChange change={0.change} stat='{0.stat}'>".format(self)


class PastMoveStatValues:
    __slots__ = ("accuracy", "effect_chance", "power", "pp", "effect_entries", "type", "version_group")

    def __init__(self, data: dict):
        self.accuracy = data["accuracy"]
        self.effect_chance = data["effect_chance"]
        self.power = data["power"]
        self.pp = data["pp"]
        self.effect_entries = [VerboseEffect(d) for d in data["effect_entries"]]
        self.type = _pretty_format(data["type"]["name"])
        self.version_group = _pretty_format(data["version_group"]["name"])

    def __repr__(self) -> str:
        return "<PastMoveStatValues type='{0.type}' version_group='{0.version_group}'>".format(self)


class ContestComboDetail:
    __slots__ = ("use_before", "use_after")

    def __init__(self, data: dict):
        self.use_before = [_pretty_format(d["name"]) for d in data["use_before"]]
        self.use_after = [_pretty_format(d["name"]) for d in data["use_after"]]

    def __repr__(self) -> str:
        return "<ContestComboDetail use_before={0.use_before} use_after={0.use_after}>".format(self)


class ContestComboSet:
    __slots__ = ("normal", "super")

    def __init__(self, data: dict):
        self.normal = ContestComboDetail(data["normal"])
        self.super = ContestComboDetail(data["super"])

    def __repr__(self):
        return "<ContestComboSet normal={0.normal} super={0.super}>".format(self)
