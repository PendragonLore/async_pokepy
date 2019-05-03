# -*- coding: utf-8 -*-

from .http import HTTPPokemonClient
from .types import Pokemon, Sprite, Move, Ability
from typing import Union


class Client:
    def __init__(self, http_client: HTTPPokemonClient):
        self._http = http_client
        self.loop = http_client.loop

        self.pokemons = {}
        self.moves = {}
        self.abilitys = {}  # this "typo" makes it easier to access the cache

    @classmethod
    async def connect(cls, *, loop=None):
        http = HTTPPokemonClient(loop)
        await http.connect()
        return cls(http)

    def clear(self):
        self.pokemons = {}
        self.moves = {}
        self.abilitys = {}

    async def close(self):
        self.clear()
        await self._http.close()
        del self

    def _add_to_cache(self, which: str, obj: Union[Pokemon, Ability, Move]):
        cache = getattr(self, which + "s", None)
        cache[obj.name] = obj

    def _format(self, thing: str) -> str:
        if thing.lower() in ("oh-ho", "porygon-z"):
            return thing.capitalize()
        return thing.replace("-", " ").title()

    def _format_tuple(self, r, thing: str, full_thing: str) -> tuple:
        return tuple(self._format(t.get(thing).get("name")) for t in reversed(r.get(full_thing)))

    async def get_pokemon(self, name: str) -> Pokemon:
        cache_check = self.pokemons.get(self._format(name))
        if cache_check is not None:
            return cache_check

        r = await self._http.get_pokemon(name)
        data = dict()

        data["name"] = self._format(r["name"])
        data["id"] = r["id"]
        data["weight"] = r["weight"]
        data["height"] = r["height"]
        data["stats"] = tuple(s.get("base_stat") for s in reversed(r.get("stats")))
        data["types"] = self._format_tuple(r, "type", "types")
        data["moves"] = self._format_tuple(r, "move", "moves")
        data["abilities"] = self._format_tuple(r, "ability", "abilities")
        data["held_items"] = self._format_tuple(r, "item", "held_items")
        data["sprites"] = {k: Sprite(v, self._http) for k, v in r.get("sprites").items()}

        ret = Pokemon(data)
        self._add_to_cache("pokemon", ret)

        return ret

    async def get_move(self, name: str) -> Move:
        cache_check = self.moves.get(self._format(name))
        if cache_check is not None:
            return cache_check

        r = await self._http.get_move(name)
        data = dict()

        data["name"] = self._format(r["name"])
        data["id"] = r["id"]
        data["accuracy"] = r["accuracy"]
        data["effect_chance"] = r["effect_chance"]
        data["pp"] = r["pp"]
        data["priority"] = r["priority"]
        data["power"] = r["power"]
        data["damage_class"] = self._format(r["damage_class"]["name"])
        data["type"] = self._format(r["type"]["name"])
        data["target"] = self._format(r["target"]["name"])
        data["generation"] = self._format(r["generation"]["name"])
        data["flavor_text_entries"] = tuple(e["flavor_text"] for e in r["flavor_text_entries"])
        data["effect"] = tuple(o["effect"] for o in r["effect_entries"])
        data["short_effect"] = tuple(o["short_effect"] for o in r["effect_entries"])

        ret = Move(data)
        self._add_to_cache("ability", ret)

        return ret

    async def get_ability(self, name: str):
        cache_check = self.abilitys.get(self._format(name))
        if cache_check is not None:
            return cache_check

        r = await self._http.get_ability(name)
        data = dict()

        data["name"] = self._format(r["name"])
        data["id"] = r["id"]
        data["is_main_series"] = r["is_main_series"]
        data["effect"] = tuple(o["effect"] for o in r["effect_entries"])
        data["short_effect"] = tuple(o["short_effect"] for o in r["effect_entries"])
        data["generation"] = self._format(r["generation"]["name"])
        data["pokemon"] = tuple(self._format(p["pokemon"]["name"]) for p in r["pokemon"])

        ret = Ability(data)
        self._add_to_cache("ability", ret)

        return ret
