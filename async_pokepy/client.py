# -*- coding: utf-8 -*-

from .http import HTTPPokemonClient
from .types import Pokemon
from .utils import _fmt_param
from typing import Union


class Client:
    """The client representing a connection with the API.

    You must use :meth:`~Client.connect` to initiate the class.

    Attributes
    ----------
    loop: :class:`asyncio.AbstractEventLoop`
        The event loop used for HTTP requests.
    """
    __slots__ = ("_http", "loop", "_cache_pokemon")

    def __init__(self, http_client: HTTPPokemonClient):
        self._http = http_client
        self.loop = http_client.loop

        self.clear()

    @classmethod
    async def connect(cls, *, loop=None):
        """Connect to the PokeAPI.

        You **must** use this classmethod to connect.

        Parameters
        ----------
        loop: Optional[:class:`asyncio.AbstractEventLoop`]
            The event loop used for HTTP requests, if no loop is provided
            :func:`asyncio.get_event_loop` is used."""
        http = HTTPPokemonClient(loop)
        await http.connect()
        return cls(http)

    def clear(self):
        """Clear the cache."""
        self._cache_pokemon = {}

    async def close(self):
        """Close the connection to the API and clear the cache.

        Use this when cleaning up."""
        self.clear()
        await self._http.close()
        del self

    def _add_to_cache(self, which: str, obj: Union[Pokemon]):
        cache = getattr(self, "_cache_" + which)
        cache[_fmt_param(obj.name)] = obj

    async def get_pokemon(self, name: str) -> Pokemon:
        """Get a :class:`Pokemon` from the API,
        at the moment it's not possible to search by :attr:`~Pokemon.id` due to caching issues.

        The Pokémon will be cached.

        Parameters
        ----------
        name: :class:`str`
            The name of the Pokèmon.

        Raises
        ------
        PokeAPIException
            The request failed.
        NotFound
            The Pokémon was not found.
        RateLimited
            More then 100 requests in one minute.

        Returns
        -------
        :class:`Pokemon`
            The Pokèmon searched for."""
        cache_check = self._cache_pokemon.get(_fmt_param(name))
        if cache_check is not None:
            return cache_check

        r = await self._http.get_pokemon(name)

        ret = Pokemon(r)
        self._add_to_cache("pokemon", ret)

        return ret
