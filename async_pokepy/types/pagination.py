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
import typing

from ..exceptions import NoMoreItems
from .abc import AsyncIterator

__all__ = ("AsyncPaginationIterator",)


class AsyncPaginationIterator(AsyncIterator):
    """Represents an async iterator iterating over a pagination of resources.

    .. container:: operations

        .. describe:: async for x in y

            Iterates over the contents of the async iterator.

    .. versionadded:: 0.1.0a"""
    __slots__ = ("limit", "offset", "thing", "can_iter", "_http", "queue")

    def __init__(self, http, thing: str, limit: int = 20, offset: int = 0):
        if limit < 1 or offset < 0:
            raise ValueError("Limit or offset cannot be negative.")

        self.limit = limit
        self.offset = offset
        self.thing = thing

        self.can_iter = True
        self._http = http

        self.queue = asyncio.Queue()

    async def next(self) -> typing.Any:
        """Get the next resource from the iterator.

        Raises
        ------
        NoMoreItems
            There are no more items left.

        Returns
        -------
        :class:`~typing.Any`
            The resource."""
        if self.queue.empty():
            await self.fill_queue()

        try:
            return self.queue.get_nowait()
        except asyncio.QueueEmpty:
            raise NoMoreItems()

    async def fill_queue(self):
        if self.can_iter:
            data = await self._http.get_pagination(self.thing, limit=self.limit, offset=self.offset)

            if not data["results"]:
                raise NoMoreItems()

            for result in data["results"]:
                await self.queue.put((result["name"], int(result["url"].split("/")[-2])))

            self.can_iter = False
