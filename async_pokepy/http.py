# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import logging
import typing
import sys

from .exceptions import PokeAPIException, RateLimited, NotFound, Forbidden
from .utils import _fmt_param

log = logging.getLogger(__name__)


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
                async with self._session.get(url, **params) as r:
                    log.info("{0} {1} returned {2} status code".format(r.method, r.url, r.status))

                    data = await r.json() if "application/json" in r.headers["Content-Type"] else await r.text()

                    if 300 > r.status >= 200:
                        log.info("{0} {1} succeeded".format(r.method, r.url))
                        return data

                    if r.status == 429:
                        log.error("Surpassed 100 API requests in one minute")
                        raise RateLimited(r, "Surpassed 100 API requests in one minute.")

                    if r.status in {500, 502}:
                        sleep_time = 1 + tries * 2
                        log.warning("Internal API error, retrying in {0}".format(sleep_time))
                        await asyncio.sleep(sleep_time, loop=self.loop)
                        continue

                    if r.status == 403:
                        raise Forbidden(r, "You can't access this endpoint.")
                    elif r.status == 404:
                        raise NotFound(r, "This endpoint was not found.")
                    else:
                        raise PokeAPIException(r, "Uncaught status code.")

            log.critical("Out of requests tries.")
            raise PokeAPIException(r, "Out of tries.")

    async def connect(self):
        self._session = aiohttp.ClientSession(headers=self.headers, loop=self.loop)

    async def close(self):
        await self._session.close()
        del self

    async def download_sprite(self, url: str) -> bytes:
        async with self._session.get(url) as resp:
            if resp.status == 200:
                return await resp.read()
            elif resp.status == 404:
                raise NotFound(resp, "Sprite not found.")
            elif resp.status == 403:
                raise Forbidden(resp, "Cannot retrieve sprite.")
            else:
                raise PokeAPIException(resp, "Failed to get sprite.")

    def get_pokemon(self, name: str) -> typing.Coroutine:
        return self.request("/pokemon/{0}".format(_fmt_param(name)))

    def get_move(self, name: str) -> typing.Coroutine:
        return self.request("/move/{0}".format(_fmt_param(name)))

    def get_ability(self, name: str) -> typing.Coroutine:
        return self.request("/ability/{0}".format(_fmt_param(name)))
