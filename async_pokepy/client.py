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
from .types import Pokemon
from .utils import _fmt_param


class Client:
    """The client representing a connection with the API.

    You must use :meth:`~Client.connect` to initiate the class.

    Attributes
    ----------
    loop: :class:`asyncio.AbstractEventLoop`
        The event loop used for HTTP requests.
    """
    __slots__ = ("_http", "loop", "cache_pokemon")

    def __init__(self, http_client: HTTPPokemonClient):
        self._http = http_client
        self.loop = http_client.loop

        self.clear()

    @classmethod
    async def connect(cls, base: str = None, user_agent: str = None, *, loop=None):
        """Connect to the PokeAPI.

        You **must** use this classmethod to connect.

        Parameters
        ----------
        base: Optional[:class:`str`]
            The base to use for all API requests, userful to edit if you
            want to host your own instance of the API.
            Defaults to `https://pokeapi.co/api/v2`.
        user_agent: Optional[:class:`str`]
            The User-Agent header to use when making requests.
        loop: Optional[:class:`asyncio.AbstractEventLoop`]
            The event loop used for HTTP requests, if no loop is provided
            :func:`asyncio.get_event_loop` is used to get one."""
        http = HTTPPokemonClient(loop=loop, user_agent=user_agent, base=base)
        await http.connect()

        return cls(http)

    def clear(self):
        """Clear the cache."""
        self.cache_pokemon = {}

    async def close(self):
        """Close the connection to the API and clear the cache.

        Use this when cleaning up."""
        self.clear()
        await self._http.close()
        del self

    @staticmethod
    def _add_to_cache(cache: dict, obj: Union[Pokemon]):
        cache[(_fmt_param(obj.name), obj.id)] = obj

    @staticmethod
    def _get_from_cache(cache: dict, query: Union[int, str]):
        cache_friendly_name = None

        if isinstance(query, str):
            if query.isdigit():
                cache_friendly_name = int(query)
            else:
                cache_friendly_name = _fmt_param(query)

        for key, value in cache.items():  # Necessary for searching by both ID and name.
            if (cache_friendly_name or query) in key:
                return value

        return None

    async def get_pokemon(self, query: Union[int, str]) -> Pokemon:
        """Get a :class:`Pokemon` from the API.

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

        check = self._get_from_cache(self.cache_pokemon, query)
        if check:
            return check

        data = await self._http.get_pokemon(query)

        ret = Pokemon(data)
        self._add_to_cache(self.cache_pokemon, ret)

        return ret

    async def save_sprite(self, url: str, fp, *, seek_begin: bool = True) -> int:
        """Save a sprite url into a file-like object.

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
            The number of bytes written.
        """
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

        Parameters
        ----------
        url: :class:`str`
            The image url of the sprite.

        Returns
        -------
        :class:`bytes`
            The bytes read.
        """
        return await self._http.download_sprite(url)
