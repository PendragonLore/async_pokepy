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
from .other import VersionGameIndex


class Pokemon(BaseObject):
    """Represents a Pokémon object.

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
        The PokeAPI identifier for this Pokémon.
    name: :class:`str`
        The name for this Pokémon.
    base_experience: :class:`int`
        The base experience gained for defeating this Pokémon.
    height: :class:`int`
        The height of this Pokémon, in decimetres.
    is_default: :class:`bool`
        ``True`` if this Pokémon is used as the default for each species.
    order: :class:`int`
        Order for sorting. Almost national order, except families are grouped together.
    weight: :class:`id`
        The weight of this Pokémon, in hectograms.
    abilities: List[:class:`PokemonAbility`]
        A list of :class:`PokemonAbility` this Pokémon could potentially have.
    moves: List[:class:`PokemonMove`]
        A list of moves along with learn methods and level details pertaining to specific version groups.
    forms: List[:class:`str`]
        A list of forms this Pokémon can take on.
    game_indices: List[:class:`VersionGameIndex`]
        A list of :class:`VersionGameIndex` relevent to Pokémon item by generation.
    stats: List[:class:`PokemonStat`]
        A list of base stat values for this Pokémon.
    types:  List[:class:`PokemonType`]
        A list of details showing types this Pokémon has.
    sprites: :class:`PokemonSprites`
        A set of sprites used to depict this Pokémon in the game.
    """
    __slots__ = (
        "stats", "types", "weight", "moves", "abilities", "height",
        "sprites", "held_items", "base_experience", "is_default", "order",
        "species", "forms", "game_indices"
    )

    def __init__(self, data: dict):
        super().__init__(data)

        self.base_experience = data["base_experience"]
        self.weight = data["weight"]
        self.height = data["height"]
        self.stats = data["stats"]
        self.is_default = data["is_default"]
        self.order = data["order"]

        self.species = data["species"]["name"]
        self.forms = [_pretty_format(d["name"]) for d in data["forms"]]

        self.sprites = PokemonSprites(data["sprites"])

        self.abilities = [PokemonAbility(d) for d in data["abilities"]]
        self.types = [PokemonType(d) for d in data["types"]]
        self.moves = [PokemonMove(d) for d in data["moves"]]
        self.stats = [PokemonStat(d) for d in data["stats"]]
        self.held_items = [PokemonHeldItem(d) for d in data["held_items"]]
        self.game_indices = [VersionGameIndex(d) for d in data["game_indices"]]

    def __repr__(self) -> str:
        return "<Pokemon id={0.id} name='{0}'>".format(self)


class PokemonStat:
    """Represents a partial Stat object bound to a :class:`Pokemon`.

    Attributes
    ----------
    stat: :class:`str`
        The name of the stat.
    effort: :class:`int`
        The effort points (EV) the Pokémon has in the stat.
    base_stat: :class:`int`
        The base value of the stat.
    """
    __slots__ = ("stat", "effort", "base_stat")

    def __init__(self, data: dict):
        self.stat = _pretty_format(data["stat"]["name"])
        self.effort = data["effort"]
        self.base_stat = data["base_stat"]

    def __repr__(self):
        return "<PokemonStat stat='{0.stat}' effort={0.effort} base_stat={0.base_stat}>".format(self)


class PokemonAbility:
    """Represents a partial Ability object bound to a :class:`Pokemon`.

    .. container:: operations

        .. describe:: str(x)

            Returns the ability's name.

    Attributes
    ----------
    ability: :class:`str`
        The ability's name.
    slot: :class:`int`
        The slot this ability occupies in the Pokémon species.
    is_hidden: :class:`bool`
        Whether or not this is a hidden ability."""
    __slots__ = ("is_hidden", "slot", "ability")

    def __init__(self, data: dict):
        self.is_hidden = data["is_hidden"]
        self.slot = data["slot"]
        self.ability = _pretty_format(data["ability"]["name"])

    def __str__(self) -> str:
        return self.ability

    def __repr__(self) -> str:
        return "<PokemonAbility ability='{0}' is_hidden={0.is_hidden} slot={0.slot}>".format(self)


class PokemonType:
    """Represents a partial Type object bound to a :class:`Pokemon`.

    .. container:: operations

        .. describe:: str(x)

            Returns the type's name.

    Attributes
    ----------
    type: :class:`str`
        The name of the type the Pokémon has.
    slot: :class:`int`
        The order the Pokémon's types are listed in."""
    __slots__ = ("type", "slot")

    def __init__(self, data: dict):
        self.type = _pretty_format(data["type"]["name"])
        self.slot = data["slot"]

    def __str__(self) -> str:
        return self.type

    def __repr__(self):
        return "<PokemonType type='{0}' slot={0.slot}>".format(self)


class PokemonSprites:
    """Represents all of the possible sprites a :class:`Pokemon` could have.

    .. note::
        All of these attributes could be ``None`` or a friendly image url of the described sprite.

    Attributes
    ----------
    front_default: Optional[:class:`str`]
        The default sprite of a Pokémon from the front in battle.
    front_shiny: Optional[:class:`str`]
        The shiny sprite of a Pokémon from the front in battle.
    front_female: Optional[:class:`str`]
        The female sprite of a Pokémon from the front in battle.
    front_shiny_female: Optional[:class:`str`]
        The shiny female sprite of a Pokémon from the front in battle.
    back_default: Optional[:class:`str`]
        The default sprite of a Pokémon from the back in battle.
    back_shiny: Optional[:class:`str`]
        The shiny sprite of a Pokémon from the back in battle.
    back_female: Optional[:class:`str`]
        The female sprite of a Pokémon from the back in battle.
    back_shiny_female: Optional[:class:`str`]
        The shiny sprite depiction of a Pokémon from the back in battle.
    """
    __slots__ = (
        "front_default", "front_shiny", "front_female", "front_shiny_female",
        "back_default", "back_shiny", "back_female", "back_shiny_female"
    )

    def __init__(self, data: dict):
        self.front_default = data["front_default"]
        self.front_shiny = data["front_shiny"]
        self.front_female = data["front_female"]
        self.front_shiny_female = data["front_shiny_female"]

        self.back_default = data["back_default"]
        self.back_shiny = data["back_shiny"]
        self.back_female = data["back_female"]
        self.back_shiny_female = data["back_shiny_female"]


class PokemonMove:
    """Represents a partial Move object bound to a :class:`Pokemon`

    .. container:: operations

        .. describe:: str(x)

            Returns the move's name.

    Attributes
    ----------
    move: :class:`str`
        The name of the move the Pokémon can learn.
    version_group_details: List[:class:`PokemonMoveVersion`]
        The details of the version in which the Pokémon can learn the move.
    """
    __slots__ = ("move", "version_group_details")

    def __init__(self, data: dict):
        self.move = _pretty_format(data["move"]["name"])
        self.version_group_details = [PokemonMoveVersion(d) for d in data["version_group_details"]]

    def __str__(self) -> str:
        return self.move

    def __repr__(self) -> str:
        return "<PokemonMove move='{0.move}' version_group_details={0.version_group_details}>".format(self)


class PokemonMoveVersion:
    """Represents a partial Version object bound to a :class:`PokemonMove`.

    Attributes
    ----------
    move_learn_method: :class:`str`
        The name of the method by which the move is learned.
    version_group: :class:`str`
        The name of the version group in which the move is learned.
    level_learned_at: :class:`int`
        The minimum level to learn the move."""
    __slots__ = ("move_learn_method", "version_group", "level_learned_at")

    def __init__(self, data: dict):
        self.level_learned_at = data["level_learned_at"]
        self.version_group = _pretty_format(data["version_group"]["name"])
        self.move_learn_method = _pretty_format(data["move_learn_method"]["name"])

    def __repr__(self) -> str:
        return ("<PokemonMoveVersion move_learn_method='{0.move_learn_method}' level_learned_at={0.level_learned_at}>"
                .format(self))


class PokemonHeldItem:
    """Represents a partial Item object bound to a :class:`Pokemon`.

    .. container:: operations

        .. describe:: str(x)

            Returns the ability's name.

    Attributes
    ----------
    item: :class:`str`
        The item the bound Pokémon holds.
    version_details: List[:class:`PokemonHeldItemVersion`]
        The details of the different versions in which the item is held."""
    __slots__ = ("item", "version_details")

    def __init__(self, data: dict):
        self.item = _pretty_format(data["item"]["name"])
        self.version_details = [PokemonHeldItemVersion(d) for d in data["version_details"]]

    def __str__(self) -> str:
        return self.item

    def __repr__(self) -> str:
        return "<PokemonHeldItem item='{0}' version_details={0.version_details}>".format(self)


class PokemonHeldItemVersion:
    """Represents a partial Version object bound to a :class:`PokemonHeldItem`.

    Attributes
    ----------
    version: :class:`str`
        The version bound to the held item.
    rarity: :class:`int`
        How often the item is held."""
    __slots__ = ("version", "rarity")

    def __init__(self, data: dict):
        self.version = _pretty_format(data["version"]["name"])
        self.rarity = data["rarity"]

    def __repr__(self) -> str:
        return "<PokemonHeldItemVersion version={0.version} rarity={0.rarity}>".format(self)
