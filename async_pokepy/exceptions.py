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


class PokemonException(Exception):
    """The base exception for this wrapper."""


class PokeAPIException(PokemonException):
    """Exception raised when an HTTP request is not successful.

    Attributes
    ----------
    response: :class:`aiohttp.ClientResponse`
        The failed HTTP response.
    status: :class:`int`
        The HTTP status code.
    message: :class:`str`
        A, hopefully, useful exception message."""

    def __init__(self, response, message: str):
        self.response = response
        self.status = response.status

        self.message = "API responded with status code {0} {2}: {1}".format(self.status, message, response.reason)

        super().__init__(self.message)


class RateLimited(PokeAPIException):
    """Exception raised when an HTTP request is equal to 429 TOO MANY REQUESTS.

    This exception will only raise if you surpass 100 requests per minutes,
    if you need more requests then that it would be better to host your own
    API instance.

    This inherits from :exc:`PokeAPIException`."""


class NotFound(PokeAPIException):
    """Exception raised when an HTTP request response code is equal to 404 NOT FOUND.

    This inherits from :exc:`PokeAPIException`."""


class Forbidden(PokeAPIException):
    """Exception raised when an HTTP request response code is equal to 403 FORBIDDEN.

    This inherits from :exc:`PokeAPIException`."""
