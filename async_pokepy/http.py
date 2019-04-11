# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import logging
import sys

from .exceptions import PokeAPIException, RateLimited, NotFound, Forbidden

log = logging.getLogger(__name__)


class HTTPPokemonClient:
    BASE = "https://pokeapi.co/api/v2"

    def __init__(self, loop=None):
        self.loop = asyncio.get_event_loop() if not loop else loop
        self.headers = {
            "User-Agent": "Python/{0[0]}.{0[1]} aiohttp/{1}".format(sys.version_info, aiohttp.__version__)
        }
        self._session = None

    def fmt_param(self, thing):
        return "-".join(thing.lower().split())

    async def request(self, method, url, **params):
        url = (self.BASE + url)
        for tries in range(5):
            async with self._session.request(method, url, **params) as r:
                log.info("{0} {1} returned {2} status code".format(method, url, r.status))

                data = await r.json() if "application/json" in r.headers["Content-Type"] else await r.text()

                if 300 > r.status >= 200:
                    log.info("{0} {1} succeed".format(method, url))
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

    async def download_sprite(self, url):
        async with self._session.get(url) as resp:
            if resp.status == 200:
                return await resp.read()
            elif resp.status == 404:
                raise NotFound(resp, "Sprite not found.")
            elif resp.status == 403:
                raise Forbidden(resp, "Cannot retrieve asset.")
            else:
                raise PokeAPIException(resp, "Failed to get sprite.")

    def get_pokemon(self, name: str):
        return self.request("GET", "/pokemon/{0}".format(self.fmt_param(name)))

    def get_move(self, name: str):
        return self.request("GET", "/move/{0}".format(self.fmt_param(name)))

    def get_ability(self, name: str):
        return self.request("GET", "/ability/{0}".format(self.fmt_param(name)))
