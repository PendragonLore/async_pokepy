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

from .abc import BaseObject
from .common import NamedAPIObject, VersionGameIndex, Name

__all__ = (
    "Pokemon",
    "PokemonStat",
    "PokemonAbility",
    "PokemonType",
    "PokemonSprites",
    "PokemonMove",
    "PokemonMoveVersion",
    "PokemonHeldItem",
    "PokemonHeldItemVersion",
    "PokemonColor",
    "PokemonHabitat"
)


class Pokemon(BaseObject):
    """Represents a Pokémon object from the API.

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
        The PokeAPI identifier for the Pokémon.
    name: :class:`str`
        The name for the Pokémon.
    base_experience: :class:`int`
        The base experience gained for defeating the Pokémon.
    height: :class:`int`
        The height of the Pokémon, in decimetres.
    is_default: :class:`bool`
        ``True`` if the Pokémon is used as the default for each species.
    order: :class:`int`
        Order for sorting. Almost national order, except families are grouped together.
    weight: :class:`id`
        The weight of the Pokémon, in hectograms.
    abilities: List[:class:`PokemonAbility`]
        A list of :class:`PokemonAbility` the Pokémon could potentially have.
    moves: List[:class:`PokemonMove`]
        A list of moves along with learn methods and level details pertaining to specific version groups.
    forms: List[:class:`NamedAPIObject`]
        A list of forms the Pokémon can take on.
    game_indices: List[:class:`VersionGameIndex`]
        A list of :class:`VersionGameIndex` relevent to Pokémon item by generation.
    stats: List[:class:`PokemonStat`]
        A list of base stat values for the Pokémon.
    types:  List[:class:`PokemonType`]
        A list of details showing types the Pokémon has.
    sprites: :class:`PokemonSprites`
        A set of sprites used to depict the Pokémon in the game.
    species: :class:`NamedAPIObject`
        The species the Pokémon belongs to."""
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

        self.species = NamedAPIObject(data["species"])
        self.forms = [NamedAPIObject(d) for d in data["forms"]]

        self.sprites = PokemonSprites(data["sprites"])

        self.abilities = [PokemonAbility(d) for d in data["abilities"]]
        self.types = [PokemonType(d) for d in data["types"]]
        self.moves = [PokemonMove(d) for d in data["moves"]]
        self.stats = [PokemonStat(d) for d in data["stats"]]
        self.held_items = [PokemonHeldItem(d) for d in data["held_items"]]
        self.game_indices = [VersionGameIndex(d) for d in data["game_indices"]]


class PokemonStat:
    """Represents a stat of a :class:`Pokemon`.

    Attributes
    ----------
    stat: :class:`NamedAPIObject`
        The stat.
    effort: :class:`int`
        The effort points (EV) the Pokémon has in the stat.
    base_stat: :class:`int`
        The base value of the stat.
    """
    __slots__ = ("stat", "effort", "base_stat")

    def __init__(self, data: dict):
        self.stat = NamedAPIObject(data["stat"])
        self.effort = data["effort"]
        self.base_stat = data["base_stat"]

    def __repr__(self):
        return "<PokemonStat stat='{0.stat}' effort={0.effort} base_stat={0.base_stat}>".format(self)


class PokemonAbility:
    """Represents an ability of a :class:`Pokemon`.

    .. container:: operations

        .. describe:: str(x)

            Returns the ability's name.

    Attributes
    ----------
    ability: :class:`NamedAPIObject`
        The ability.
    slot: :class:`int`
        The slot the ability occupies in the Pokémon species.
    is_hidden: :class:`bool`
        Whether or not the ability is hidden."""
    __slots__ = ("is_hidden", "slot", "ability")

    def __init__(self, data: dict):
        self.is_hidden = data["is_hidden"]
        self.slot = data["slot"]
        self.ability = NamedAPIObject(data["ability"])

    def __str__(self) -> str:
        return str(self.ability)

    def __repr__(self) -> str:
        return "<PokemonAbility ability='{0}' is_hidden={0.is_hidden} slot={0.slot}>".format(self)


class PokemonType:
    """Represents a type of a :class:`Pokemon`.

    .. container:: operations

        .. describe:: str(x)

            Returns the type's name.

    Attributes
    ----------
    type: :class:`NamedAPIObject`
        The type the Pokémon has.
    slot: :class:`int`
        The order the Pokémon's types are listed in."""
    __slots__ = ("type", "slot")

    def __init__(self, data: dict):
        self.type = NamedAPIObject(data["type"])
        self.slot = data["slot"]

    def __str__(self) -> str:
        return str(self.type)

    def __repr__(self):
        return "<PokemonType type='{0}' slot={0.slot}>".format(self)


class PokemonSprites:
    """Represents all of the possible sprites a :class:`Pokemon` could have.

    .. note::
        All of these attributes could be ``None`` or a friendly image url of the described sprite.

    .. container:: operations

        .. describe:: for x in y

            Returns an iterator over the sprites.

        .. describe:: list(x)

            Returns all of the sprites as a list, this will consume the iterator.

        .. describe:: len(x)

            Returns the number of sprites that are **not** ``None``.

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
        The shiny sprite depiction of a Pokémon from the back in battle."""
    __slots__ = (
        "front_default", "front_shiny", "front_female", "front_shiny_female",
        "back_default", "back_shiny", "back_female", "back_shiny_female", "__iter", "__sprites"
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

        self.__sprites = [value for value in data.values()]
        self.__iter = iter(self.__sprites)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.__iter)

    def __len__(self) -> int:
        return len([x for x in self.__sprites if x is not None])


class PokemonMove:
    """Represents a move of a :class:`Pokemon.`

    .. container:: operations

        .. describe:: str(x)

            Returns the move's name.

    Attributes
    ----------
    move: :class:`NamedAPIObject`
        The move the Pokémon can learn.
    version_group_details: List[:class:`PokemonMoveVersion`]
        The details of the version in which the Pokémon can learn the move.
    """
    __slots__ = ("move", "version_group_details")

    def __init__(self, data: dict):
        self.move = NamedAPIObject(data["move"])
        self.version_group_details = [PokemonMoveVersion(d) for d in data["version_group_details"]]

    def __str__(self) -> str:
        return str(self.move)

    def __repr__(self) -> str:
        return "<PokemonMove move='{0.move}' version_group_details={0.version_group_details}>".format(self)


class PokemonMoveVersion:
    """Represents the version of a :class:`PokemonMove`

    Attributes
    ----------
    move_learn_method: :class:`NamedAPIObject`
        The method by which the move is learned.
    version_group: :class:`NamedAPIObject`
        The version group in which the move is learned.
    level_learned_at: :class:`int`
        The minimum level to learn the move."""
    __slots__ = ("move_learn_method", "version_group", "level_learned_at")

    def __init__(self, data: dict):
        self.level_learned_at = data["level_learned_at"]
        self.version_group = NamedAPIObject(data["version_group"])
        self.move_learn_method = NamedAPIObject(data["move_learn_method"])

    def __repr__(self) -> str:
        return ("<PokemonMoveVersion move_learn_method='{0.move_learn_method}' level_learned_at={0.level_learned_at}>"
                .format(self))


class PokemonHeldItem:
    """Represents an item held by a :class:`Pokemon`.

    .. container:: operations

        .. describe:: str(x)

            Returns the ability's name.

    Attributes
    ----------
    item: :class:`NamedAPIObject`
        The item the Pokémon holds.
    version_details: List[:class:`PokemonHeldItemVersion`]
        The details of the different versions in which the item is held."""
    __slots__ = ("item", "version_details")

    def __init__(self, data: dict):
        self.item = NamedAPIObject(data["item"])
        self.version_details = [PokemonHeldItemVersion(d) for d in data["version_details"]]

    def __str__(self) -> str:
        return str(self.item)

    def __repr__(self) -> str:
        return "<PokemonHeldItem item='{0}' version_details={0.version_details}>".format(self)


class PokemonHeldItemVersion:
    """Represents the version of a :class:`PokemonHeldItem`.

    Attributes
    ----------
    version: :class:`NamedAPIObject`
        The version bound to the held item.
    rarity: :class:`int`
        How often the item is held."""
    __slots__ = ("version", "rarity")

    def __init__(self, data: dict):
        self.version = NamedAPIObject(data["version"])
        self.rarity = data["rarity"]

    def __repr__(self) -> str:
        return "<PokemonHeldItemVersion version={0.version} rarity={0.rarity}>".format(self)


class PokemonColor(BaseObject):
    """Represents the color of a :class:`Pokemon` used for sorting one in a Pokédex.

    .. versionadded:: 0.1.7a

    .. container:: operations

        .. describe:: str(x)

            Returns the color's name.

        .. describe:: x[y]

            Returns a color's y attribute.

        .. describe:: x == y

            Check if two colors are the same.

        .. describe:: x != y

            Check if two colors are *not* the same.

    Attributes
    ----------
    id: :class:`int`
        The identifier for the color.
    name: :class:`str`
        The name of the color.
    names: List[:class:`Name`]
        The names of the color listed in different languages.
    pokemon_species: :class:`NamedAPIObject`
        A list of the Pokémon species that have the color."""
    __slots__ = ("names", "pokemon_species")

    def __init__(self, data: dict):
        super().__init__(data)

        self.names = [Name(d) for d in data["names"]]
        self.pokemon_species = [NamedAPIObject(d) for d in data["pokemon_species"]]


class PokemonHabitat(BaseObject):
    """Represents an habitat of a :class:`Pokemon`.

    .. versionadded:: 0.1.7a

    .. container:: operations

        .. describe:: str(x)

            Returns the habitat's name.

        .. describe:: x[y]

            Returns a habitat's y attribute.

        .. describe:: x == y

            Check if two habitats are the same.

        .. describe:: x != y

            Check if two habitats are *not* the same.

    Attributes
    ----------
    id: :class:`int`
        The identifier for the habita.
    name: :class:`str`
        The name of the habitat.
    names: List[:class:`Name`]
        The names of the habitat listed in different languages.
    pokemon_species: List[:class:`NamedAPIObject`]
        A list of the Pokémon species that can be found in the habitat."""
    __slots__ = ("names", "pokemon_species")

    def __init__(self, data: dict):
        super().__init__(data)

        self.names = [Name(d) for d in data["names"]]
        self.pokemon_species = [NamedAPIObject(d) for d in data["pokemon_species"]]
