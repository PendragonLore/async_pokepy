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

import functools
import warnings
from inspect import isawaitable
from typing import Union
from urllib.parse import quote

try:
    from lru import LRU
except ImportError:
    LRU = None

__all__ = ()


def _fmt_param(thing: Union[int, str]) -> str:
    if isinstance(thing, int):
        return str(thing)

    return quote("-".join(thing.lower().split()), safe="")


def _pretty_format(thing: str) -> str:
    if thing.lower() in ("oh-ho", "porygon-z"):
        return thing.capitalize()
    return thing.replace("-", " ").title()


def _make_cache_key(key):
    if isinstance(key, str):
        if key.isdigit():
            return int(key)

        return _fmt_param(key)

    return key


def cached(maxsize: int, with_name: bool = True):
    def outer(func):
        @functools.wraps(func)
        async def inner(cls, query: Union[int, str]):  # Very specific but it works and will work for most get_ methods
            query = _make_cache_key(query)

            for key, value in cache.items():
                if query in key:
                    return value

            val = await func(cls, query)
            if with_name:
                cache[(_make_cache_key(val.name), _make_cache_key(val.id))] = val
            else:
                cache[(_make_cache_key(val.id),)] = val

            return val

        if LRU:
            cache = LRU(maxsize)
        else:
            cache = {}
            warnings.warn("lru-dict is not installed, so the cache will not have a maxsize.")

        inner.cache = cache

        return inner

    return outer


async def maybe_coroutine(f, *args, **kwargs):
    value = f(*args, **kwargs)
    if isawaitable(value):
        return await value
    return value
