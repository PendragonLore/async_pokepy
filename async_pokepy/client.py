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

import io
from typing import Union

from .http import HTTPPokemonClient
from .types import Ability, AsyncPaginationIterator, Berry, Machine, Move, Pokemon, PokemonColor, PokemonHabitat
from .utils import cached

__all__ = ("connect",)


def connect(base="https://pokeapi.co/api/v2/", **kwargs):
    """Connect to the PokeAPI.

    This method **must** be used to connect.

    This returns a context manager mixin so it's possible to both do this:

    .. code-block:: python3

        async with async_pokepy.connect() as client:
            # do stuff

    and this

    .. code-block:: python3

        try:
            client = await async_pokepy.connect()

            # do stuff
        except ...:
            # handle exceptions
        finally:
            await client.close()

    Parameters
    ----------
    base: Optional[:class:`str`]
        The base to use for all API requests, useful to edit if you
        want to host your own instance of the API.
        Defaults to ``https://pokeapi.co/api/v2/``.
    user_agent: Optional[:class:`str`]
        The User-Agent header to use when making requests.
    loop: Optional[:class:`asyncio.AbstractEventLoop`]
        The event loop used for HTTP requests, if no loop is provided
        :func:`asyncio.get_event_loop` is used to get one.
    session: Optional[:class:`aiohttp.ClientSession`]
        The client session to use during requests.

    Returns
    -------
    :class:`Client`
        The PokeAPI client."""
    return _ClientContextMixin(base, **kwargs)


class _ClientContextMixin:
    __slots__ = ("_base", "_kwargs", "_client")

    def __init__(self, base, **kwargs):
        self._base = base
        self._kwargs = kwargs

        self._client = None

    def __await__(self):
        return Client._connect(self._base, **self._kwargs).__await__()  # pylint: disable=protected-access,no-member

    async def __aenter__(self):
        self._client = await Client._connect(self._base, **self._kwargs)  # pylint: disable=protected-access

        return self._client

    async def __aexit__(self, *args):
        await self._client.close()


class Client:
    """The client representing a connection with the API.

    It's necessary to use :meth:`Connect` to initiate this class.

    Attributes
    ----------
    loop: :class:`asyncio.AbstractEventLoop`
        The event loop used for HTTP requests."""
    __slots__ = ("_http", "loop", "_image_cache")

    def __init__(self, http_client: HTTPPokemonClient):
        self._http = http_client
        self.loop = http_client.loop

        self._image_cache = {}

    @classmethod
    async def _connect(cls, base, **kwargs):
        http = HTTPPokemonClient(base, **kwargs)
        await http.connect()

        return cls(http)

    async def close(self):
        """Close the connection to the API.

        Use this when cleaning up."""
        await self._http.close()

    @cached(128)
    async def get_pokemon(self, query: Union[int, str]) -> Pokemon:
        """Get a :class:`Pokemon` from the API.
        The query can be both the name or the ID as a string or integer.

        The Pokémon will be cached.

        Parameters
        ----------
        query: Union[:class:`int`, :class:`str`]
            The name or id of the Pokèmon.

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
        data = await self._http.get_pokemon(query)

        ret = Pokemon(data)

        return ret

    @cached(128)
    async def get_move(self, query: Union[int, str]) -> Move:
        """Get a :class:`Move` from the API.
        The query can be both the name or the ID as a string or integer.

        The move will be cached.

        .. versionadded:: 0.1.0a

        Parameters
        ----------
        query: Union[:class:`int`, :class:`str`]
            The name or id of the move.

        Raises
        ------
        PokeAPIException
            The request failed.
        NotFound
            The move was not found.
        RateLimited
            More then 100 requests in one minute.

        Returns
        -------
        :class:`Move`
            The move searched for."""
        data = await self._http.get_move(query)

        ret = Move(data)

        return ret

    @cached(128)
    async def get_ability(self, query: Union[int, str]) -> Ability:
        """Get a :class:`Ability` from the API.
        The query can be both the name or the ID as a string or integer.

        The ability will be cached.

        .. versionadded:: 0.1.2a

        Parameters
        ----------
        query: Union[:class:`int`, :class:`str`]
            The name or id of the ability.

        Raises
        ------
        PokeAPIException
            The request failed.
        NotFound
            The ability was not found.
        RateLimited
            More then 100 requests in one minute.

        Returns
        -------
        :class:`Ability`
            The move searched for."""
        data = await self._http.get_ability(query)

        ret = Ability(data)

        return ret

    @cached(128)
    async def get_berry(self, query: Union[int, str]) -> Berry:
        """Get a :class:`Berry` from the API.
        The query can be both the name or the ID as a string or integer.

        The berry will be cached.

        .. versionadded:: 0.1.3a

        Parameters
        ----------
        query: Union[:class:`int`, :class:`str`]
            The name or id of the berry.

        Raises
        ------
        PokeAPIException
            The request failed.
        NotFound
            The berry was not found.
        RateLimited
            More then 100 requests in one minute.

        Returns
        -------
        :class:`Berry`
            The berry searched for."""
        data = await self._http.get_berry(query)

        ret = Berry(data)

        return ret

    @cached(128)
    async def get_pokemon_color(self, query: Union[int, str]) -> PokemonColor:
        """Get a :class:`PokemonColor` from the API.
        The query can be both the name or the ID as a string or integer.

        The color will be cached.

        .. versionadded:: 0.1.7a

        Parameters
        ----------
        query: Union[:class:`int`, :class:`str`]
            The name or id of the color.

        Raises
        ------
        PokeAPIException
            The request failed.
        NotFound
            The color was not found.
        RateLimited
            More then 100 requests in one minute.

        Returns
        -------
        :class:`PokemonColor`
            The color searched for."""
        data = await self._http.get_pokemon_color(query)

        ret = PokemonColor(data)

        return ret

    @cached(128)
    async def get_pokemon_habitat(self, query: Union[int, str]) -> PokemonHabitat:
        """Get a :class:`PokemonHabitat` from the API.
        The query can be both the name or the ID as a string or integer.

        The habitat will be cached.

        .. versionadded:: 0.1.7a

        Parameters
        ----------
        query: Union[:class:`int`, :class:`str`]
            The name or id of the habotat.

        Raises
        ------
        PokeAPIException
            The request failed.
        NotFound
            The habitat was not found.
        RateLimited
            More then 100 requests in one minute.

        Returns
        -------
        :class:`PokemonHabitat`
            The habitat searched for."""
        data = await self._http.get_pokemon_habitat(query)

        ret = PokemonHabitat(data)

        return ret

    @cached(128, with_name=False)
    async def get_machine(self, query: Union[int, str]) -> Machine:
        """Get a :class:`Machine` from the API.
        The query can **only** be the ID of the machine as a string or int.

        The machine will be cached.

        .. versionadded:: 0.1.5a

        Parameters
        ----------
        query: Union[:class:`int`, :class:`str`]
            The id of the machine.

        Raises
        ------
        PokeAPIException
            The request failed.
        NotFound
            The machine was not found.
        RateLimited
            More then 100 requests in one minute.

        Returns
        -------
        :class:`Machine`
            The machine searched for."""
        data = await self._http.get_machine(query)

        ret = Machine(data)

        return ret

    async def save_sprite(self, url: str, fp, *, seek_begin: bool = True) -> int:
        """Save a sprite url into a file-like object.

        .. versionadded:: 0.0.9a

        .. versionchanged:: 0.1.1a

            The sprite is now cached.

        Parameters
        ----------
        url: :class:`str`
            The image url of the sprite.
        fp: Union[:class:`io.IOBase`, :class:`os.PathLike`]
            The file-like object to save the sprite to.
            This can be both a path to a file or a BinaryIO.
        seek_begin: :class:`bool`
            Whether to seek to the beginning of the file after saving is done.

        Returns
        -------
        :class:`int`
            The number of bytes written."""
        data = await self.read_sprite(url)

        if isinstance(fp, io.IOBase) and fp.writable():
            written = fp.write(data)

            if seek_begin:
                fp.seek(0)

            return written

        with open(fp, "wb") as f:
            return f.write(data)

    async def read_sprite(self, url: str) -> bytes:
        """Read a sprite url's sprite.

        .. versionadded:: 0.0.9a

        .. versionchanged:: 0.1.1a

            The sprite is now cached.

        Parameters
        ----------
        url: :class:`str`
            The image url of the sprite.

        Returns
        -------
        :class:`bytes`
            The bytes read."""
        try:
            val = self._image_cache[url]
        except KeyError:
            val = io.BytesIO((await self._http.download_sprite(url)))

            self._image_cache[url] = val

        val.seek(0)
        return val.read()

    def get_pagination(self, obj: str, **kwargs) -> AsyncPaginationIterator:
        """Retuns an async iterator representing a pagination of objects from the API.

        .. versionadded:: 0.1.0a

        Parameters
        ----------
        obj: :class:`str`
            The name of the object.
        limit: Optional[:class:`int`]
            The amount of the objects, defaults to ``20``.
        offset: Optional[:class:`int`]
            The start position of the pagination, defaults to ``0``.

        Returns
        -------
        :class:`AsyncPaginationIterator`
            The iterator."""
        return AsyncPaginationIterator(self._http, obj, **kwargs)
