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

import asyncio
import logging
import sys
from typing import Coroutine, Union
from urllib.parse import quote

import aiohttp

from .exceptions import Forbidden, NotFound, PokeAPIException, RateLimited
from .utils import _fmt_param

LOG = logging.getLogger(__name__)

__all__ = ()


class Route:
    __slots__ = ("params", "url", "route")

    def __init__(self, base, path, *args, **kwargs):
        self.route = [_fmt_param(arg) for arg in args]
        self.params = ["{0}={1}".format(k, quote(str(v))) for k, v in kwargs.items()]

        url = (base + path + "/".join(self.route))
        if self.params:
            self.url = url + "?" + "&".join(self.params)
        else:
            self.url = url


class HTTPPokemonClient:
    __slots__ = ("loop", "headers", "_session", "_lock", "base")

    def __init__(self, loop: asyncio.AbstractEventLoop = None, base: str = None, user_agent: str = None):
        self.loop = loop or asyncio.get_event_loop()
        self._lock = asyncio.Lock(loop=self.loop)

        self.base = base or "https://pokeapi.co/api/v2"
        self.headers = {
            "User-Agent": user_agent or "Python/{0[0]}.{0[1]} aiohttp/{1}".format(sys.version_info, aiohttp.__version__)
        }
        self._session = None

    async def request(self, route, **kwargs) -> Union[str, dict]:
        async with self._lock:
            for tries in range(5):
                async with self._session.get(route.url, **kwargs) as resp:
                    LOG.info("%s %s returned %d status code", resp.method, resp.url, resp.status)

                    data = (await resp.json() if "application/json" in resp.headers["Content-Type"]
                            else await resp.text())

                    if 300 > resp.status >= 200:
                        LOG.debug("%s %s succeeded with data %s", resp.method, resp.url, data)

                        return data

                    if resp.status == 429:
                        LOG.error("Surpassed 100 API requests in one minute")

                        raise RateLimited(resp, "Surpassed 100 API requests in one minute.")

                    if resp.status in {500, 502}:
                        sleep_time = 1 + tries * 2
                        LOG.warning("Internal API error, retrying in %d", sleep_time)

                        await asyncio.sleep(sleep_time, loop=self.loop)
                        continue

                    if resp.status == 403:
                        raise Forbidden(resp, "Forbidden endpoint.")
                    if resp.status == 404:
                        raise NotFound(resp, "Endpoint not found.")

                    raise PokeAPIException(resp, "Uncaught status code.")

            LOG.critical("Request timed out")
            raise PokeAPIException(resp, "Request timed out.")

    async def connect(self):
        self._session = aiohttp.ClientSession(headers=self.headers, loop=self.loop)

    async def close(self):
        await self._session.close()
        del self

    async def download_sprite(self, url: str) -> bytes:
        async with self._session.get(url) as resp:
            if resp.status == 200:
                return await resp.read()
            if resp.status == 404:
                raise NotFound(resp, "Sprite not found.")
            if resp.status == 403:
                raise Forbidden(resp, "Cannot retrieve the sprite.")

            raise PokeAPIException(resp, "Failed to get the sprite.")

    def get_pokemon(self, query: Union[int, str]) -> Coroutine:
        return self.request(Route(self.base, "/pokemon/", query))

    def get_move(self, query: Union[int, str]) -> Coroutine:
        return self.request(Route(self.base, "/move/", query))

    def get_ability(self, query: Union[int, str]) -> Coroutine:
        return self.request(Route(self.base, "/ability/", query))

    def get_pagination(self, query: str, **kwargs) -> Coroutine:
        return self.request(Route(self.base, "/{0}/".format(_fmt_param(query)), **kwargs))
