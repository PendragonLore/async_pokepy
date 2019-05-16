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
from .common import Name, VerboseEffect

__all__ = (
    "Move",
    "MoveFlavorText",
    "MoveMetaData",
    "MoveStatChange",
    "PastMoveStatValues",
    "ContestComboDetail",
    "ContestComboSet"
)


class Move(BaseObject):
    """Represents a move object from the API.

    .. versionadded:: 0.1.0a

    .. container:: operations

        .. describe:: str(x)

            Returns the move's name.

        .. describe:: x[y]

            Returns a move's y attribute.

        .. describe:: x == y

            Check if two moves are the same.

        .. describe:: x != y

            Check if two moves are *not* the same.

    Attributes
    ----------
    id: :class:`int`
        The identifier for the move.
    name: :class:`str`
        The name for the move.
    accuracy: :class:`int`
        The percent value of how likely the move is to be successful.
    effect_chance: :class:`int`
        The percent value of how likely it is that the move's effect will happen.
    pp: :class:`int`
        Power points. The number of times the move can be used.
    power_points: :class:`int`
        An alias for pp.
    priority: :class:`int`
        A value between -8 and 8. Sets the order in which the move is executed during battle.
    power: :class:`int`
        The base power of the move with a value of 0 if it does not have a base power.
    contest_combos: :class:`ContestComboSets`
        A detail of normal and super contest combos that require the move.
    contest_type: :class:`str`
        The name of the type of appeal the move gives a Pokémon when used in a contest.
    damage_class: :class:`str`
        The name of the type of damage the move inflicts on the target, e.g. physical.
    effect_entries: List[:class:`VerboseEffect`]
        The effect of the move listed in different languages.
    flavor_text_entries: List[:class:`MoveFlavorText`]
        The flavor text of the move listed in different languages.
    generation: :class:`str`
        The name of the generation in which the move was introduced.
    meta: :class:`MoveMetaData`
        Metadata about the move.
    names: List[:class:`Name`]
        The name of the move listed in different languages.
    past_values: List[:class:`PastMoveStatValues`]
        A list of move value changes across version groups of the game.
    stat_changes: List[:class:`MoveStatChange`]
        A list of stats this move effects and how much it effects them.
    target: :class:`str`
        The name of the type of target that will receive the effects of the move.
    type: :class:`str`
        The elemental type of the move."""
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

        # add effect_changes
        self.meta = MoveMetaData(data["meta"])
        self.stat_changes = [MoveStatChange(d) for d in data["stat_changes"]]
        self.names = [Name(d) for d in data["names"]]
        self.effect_entries = [VerboseEffect(d) for d in data["effect_entries"]]
        self.flavor_text_entries = [MoveFlavorText(d) for d in data["flavor_text_entries"]]
        self.past_values = [PastMoveStatValues(d) for d in data["past_values"]]

    def __repr__(self) -> str:
        return "<Move id={0.id} name='{0}'>".format(self)


class MoveFlavorText:
    """Represents the flavor text of a move associated with a language.

    .. versionadded:: 0.1.0a

    Attributes
    ----------
    flavor_text: :class:`str`
        The localized flavor text for the move in the associated language.
    language: :class:`str`
        The name of the language this text is in.
    version_group: :class:`str`
        The name of the version group that uses this flavor text."""
    __slots__ = ("flavor_text", "language", "version_group")

    def __init__(self, data: dict):
        self.flavor_text = data["flavor_text"]
        self.language = data["language"]["name"]
        self.version_group = _pretty_format(data["version_group"]["name"])

    def __repr__(self) -> str:
        return "<MoveFlavorText language='{0.language}' version_group='{0.version_group}'>".format(self)


class MoveMetaData:
    """Represents the metadata about a move.

    .. versionadded:: 0.1.0a

    Attributes
    ----------
    ailment: :class:`str`
        The status ailment the move inflicts on it's target.
    category: :class:`str`
        The name of the category of move the move falls under, e.g. damage or ailment.
    min_hits: Optional[:class:`int`]
        The minimum number of times the move hits. ``None`` if it always only hits once.
    max_hits: Optional[:class:`int`]
        The maximum number of times the move hits. ``None`` if it always only hits once.
    min_turns: Optional[:class:`int`]
        The minimum number of turns the move continues to take effect. ``None`` if it always only lasts one turn.
    max_turns: Optional[:class:`int`]
        The maximum number of turns the move continues to take effect. ``None`` if it always only lasts one turn.
    drain: :class:`int`
        HP drain (if positive) or recoil damage (if negative), in percent of damage done.
    healing: :class:`int`
        The amount of hp gained by the attacking Pokemon, in percent of it's maximum HP.
    crit_rate: :class:`int`
        Critical hit rate bonus.
    ailment_chance: :class:`int`
        The likelihood the move will cause an ailment.
    flinch_chance: :class:`int`
        The likelihood the move will cause the target Pokémon to flinch.
    stat_chance: :class:`int`
        The likelihood the mpve will cause a stat change in the target Pokémon.
    """
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
    """Represents a stat change in a :class:`move`

    .. versionadded:: 0.1.0a

    Attributes
    ----------
    change: :class:`int`
        The amount of change.
    stat: :class:`str`
        The stat being affected."""
    __slots__ = ("change", "stat")

    def __init__(self, data: dict):
        self.change = data["change"]
        self.stat = _pretty_format(data["stat"]["name"])

    def __repr__(self) -> str:
        return "<MoveStatChange change={0.change} stat='{0.stat}'>".format(self)


class PastMoveStatValues:
    """Represents changed values of a :class:`Move` in a version group.

    .. versionadded:: 0.1.0a

    Attributes
    ----------
    accuracy: :class:`int`
        The percent value of how likely the move is to be successful.
    effect_chance: :class:`int`
        The percent value of how likely it is the moves effect will take effect.
    power: :class:`int`
        The base power of the move with a value of 0 if it does not have a base power.
    pp: :class:`int`
        Power points. The number of times the move can be used.
    effect_entries: List[:class:`VerboseEffect`]
        The effect of the move listed in different languages.
    type: :class:`str`
        The name of the elemental type of the move.
    version_group: :class:`str`
        The name of the version group in which these move stat values were in effect."""
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
    """Represents a detail of moves that can be used to grain additional
    appeal points in contests.

    .. versionadded:: 0.1.0a

    Attributes
    ----------
    use_before: List[:class:`str`]
        A list of name of moves to use before this move.
    use_after: List[:class:`str`]
        A list of name of moves to use after this move."""
    __slots__ = ("use_before", "use_after")

    def __init__(self, data: dict):
        self.use_before = [_pretty_format(d["name"]) for d in data["use_before"]]
        self.use_after = [_pretty_format(d["name"]) for d in data["use_after"]]

    def __repr__(self) -> str:
        return "<ContestComboDetail use_before={0.use_before} use_after={0.use_after}>".format(self)


class ContestComboSet:
    """Represents a set of super and normal contest combos.

    .. versionadded:: 0.1.0a

    Attributes
    ----------
    normal: :class:`ContestComboDetail`
        A detail of moves this move can be used before or after, granting additional appeal points in contests.
    super: :class:`ContestComboDetail`
        A detail of moves this move can be used before or after, granting additional appeal points in super contests."""
    __slots__ = ("normal", "super")

    def __init__(self, data: dict):
        self.normal = ContestComboDetail(data["normal"])
        self.super = ContestComboDetail(data["super"])

    def __repr__(self):
        return "<ContestComboSet normal={0.normal} super={0.super}>".format(self)
