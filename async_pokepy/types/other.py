# -*- coding: utf-8 -*-


class VersionGameIndex:
    """Represents a partial Version object bound to a GameIndex.

    Attributes
    ----------
    game_index: :class:`int`
        The internal id of a PokeAPI resource within game data.
    version: :class:`str`
        The name of the version relevant to this game index.`"""
    def __init__(self, data: dict):
        self.game_index = data["game_index"]
        self.version = data["version"]["name"]

    def __repr__(self) -> str:
        return "<VersionGameIndex game_index={0.game_index} version='{0.version}'>".format(self)
