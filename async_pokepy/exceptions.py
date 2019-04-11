# -*- coding: utf-8 -*-


class PokemonException(Exception):
    pass


class PokeAPIException(PokemonException):
    def __init__(self, response, message):
        self.response = response
        self.status = response.status

        self.message = "API responded with status code {0}: {1}".format(self.status, message)

        super().__init__(self.message)


class RateLimited(PokeAPIException):
    pass


class NotFound(PokeAPIException):
    pass


class Forbidden(PokeAPIException):
    pass
