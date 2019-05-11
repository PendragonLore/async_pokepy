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
import typing

import aiohttp

from .exceptions import PokeAPIException, RateLimited, NotFound, Forbidden
from .utils import _fmt_param

LOG = logging.getLogger(__name__)


class HTTPPokemonClient:
    __slots__ = ("loop", "headers", "_session", "_lock")

    BASE = "https://pokeapi.co/api/v2"

    def __init__(self, loop: asyncio.AbstractEventLoop = None):
        self.loop = loop or asyncio.get_event_loop()
        self.headers = {
            "User-Agent": "Python/{0[0]}.{0[1]} aiohttp/{1}".format(sys.version_info, aiohttp.__version__)
        }
        self._session = None
        self._lock = asyncio.Lock(loop=self.loop)

    async def request(self, url: str, **params) -> typing.Union[str, dict]:
        url = (self.BASE + url)

        async with self._lock:
            for tries in range(5):
                async with self._session.get(url, **params) as resp:
                    LOG.info("%s %s returned %d status code", resp.method, resp.url, resp.status)

                    data = (await resp.json() if "application/json" in resp.headers["Content-Type"]
                            else await resp.text())

                    if 300 > resp.status >= 200:
                        LOG.info("%s %s succeeded", resp.method, resp.url)
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
                        raise Forbidden(resp, "You can't access this endpoint.")
                    if resp.status == 404:
                        raise NotFound(resp, "This endpoint was not found.")

                    raise PokeAPIException(resp, "Uncaught status code.")

            LOG.critical("Out of requests tries.")
            raise PokeAPIException(resp, "Out of tries.")

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
                raise Forbidden(resp, "Cannot retrieve sprite.")

            raise PokeAPIException(resp, "Failed to get sprite.")

    def get_pokemon(self, name: str) -> typing.Coroutine:
        return self.request("/pokemon/{0}".format(_fmt_param(name)))

    def get_move(self, name: str) -> typing.Coroutine:
        return self.request("/move/{0}".format(_fmt_param(name)))

    def get_ability(self, name: str) -> typing.Coroutine:
        return self.request("/ability/{0}".format(_fmt_param(name)))
