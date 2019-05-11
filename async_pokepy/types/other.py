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
