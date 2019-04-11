# -*- coding: utf-8 -*-

import io
from .exceptions import PokemonException


class _BaseObject:
    __slots__ = ("name", "id", "_data")

    def __init__(self, data: dict):
        self._data = data

        self.id = data["id"]
        self.name = data["name"]

    def __str__(self):
        return self.name

    def __getitem__(self, item):
        return self._data.get(item)

    def to_dict(self):
        return self._data


class Pokemon(_BaseObject):
    __slots__ = ("stats", "types", "weight", "moves", "abilities", "height", "sprites", "held_items")

    def __init__(self, data: dict):
        super().__init__(data)

        self.weight = data["weight"]
        self.stats = data["stats"]
        self.abilities = data["abilities"]
        self.height = data["height"]
        self.types = data["types"]
        self.moves = data["moves"]
        self.sprites = data["sprites"]
        self.held_items = data["held_items"]

    def __repr__(self):
        return "<Pokemon id={0.id} name='{0}'>".format(self)


class Move(_BaseObject):
    __slots__ = ("damage_class", "type", "effect_chance", "target", "effect", "short_effect",
                 "accuracy", "pp", "power", "generation", "power_points", "flavor_text_entries")

    def __init__(self, data: dict):
        super().__init__(data)

        self.accuracy = data["accuracy"]
        self.damage_class = data["damage_class"]
        self.effect_chance = data["effect_chance"]
        self.power = data["power"]
        self.type = data["type"]
        self.pp = data["pp"]
        self.target = data["target"]
        self.power_points = self.pp
        self.effect = data["effect"]
        self.short_effect = data["short_effect"]
        self.flavor_text_entries = data["flavor_text_entries"]

    def __repr__(self):
        return "<Move id={0.id} name'{0}'>".format(self)


class Sprite:
    __slots__ = ("url", "_http")

    def __init__(self, url, http):
        self.url = str(url)
        self._http = http

    def __bool__(self):
        return self.url is not None

    def __repr__(self):
        return "<Sprite url='{0.url}'>".format(self)

    async def save(self, fp):
        if not self.url:
            raise PokemonException("This sprite doesn't have an URL.")

        data = await self._http.download_sprite(self.url)
        if isinstance(fp, io.IOBase) and fp.writable():
            written = fp.write(data)
            fp.seek(0)
            return written
        else:
            with open(fp, "wb") as f:
                return f.write(data)


class Ability(_BaseObject):
    __slots__ = ("is_main_series", "generation", "effect", "pokemon", "short_effect")

    def __init__(self, data):
        super().__init__(data)

        self.is_main_series = data["is_main_series"]
        self.generation = data["generation"]
        self.effect = data["effect"]
        self.short_effect = data["short_effect"]
        self.pokemon = data["pokemon"]

    def __repr__(self):
        return "<Ability id={0.id} name='{0}'>".format(self)
