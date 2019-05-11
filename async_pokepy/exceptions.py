# -*- coding: utf-8 -*-


class PokemonException(Exception):
    """The base exception for this wrapper."""
    pass


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
