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

from .abc import BaseObject
from .common import NamedAPIObject


class Berry(BaseObject):
    """Represents a berry object from the API.

    .. container:: operations

        .. describe:: str(x)

            Returns the berry's name.

        .. describe:: x[y]

            Returns a berry's y attribute.

        .. describe:: x == y

            Check if two berries are the same.

        .. describe:: x != y

            Check if two berries are *not* the same.

    Attributes
    ----------
    id: :class:`int`
        The identifier of the berry.
    name: :class:`str`
        The name of the berry.
    growth_time: :class:`int`
        The time it takes the tree to grow one stage, in hours.
        Berry trees go through four of these growth stages before they can be picked.
    max_harvest: :class:`int`
        The maximum number of these berries that can grow on one tree in Generation IV.
    natural_gift_power: :class:`int`
        The power of the move "Natural Gift" when used with the berry.
    size: :class:`int`
        The size of the berry, in millimeters.
    smoothness: :class:`int`
        The smoothness of the berry, used in making Pokéblocks or poffins.
    firmness: :class:`NamedAPIObject`
        The firmness of the berry, used in making Pokéblocks or poffins.
    soil_dryness: :class:`int`
        The speed at which the berry dries out the soil as it grows.
        A higher rate means the soil dries more quickly.
    flavors: List[:class:`BerryFlavorMap`]
        A list of references to each flavor a berry can have and the potency of
        each of those flavors in regard to the berry.
    item: :class:`NamedAPIObject`
        Reference to the item specific data for this berry.
    natural_gift_type: :class:`NamedAPIObject`
        The type inherited by "Natural Gift" when used with this Berry."""
    __slots__ = (
        "growth_time", "max_harvest", "natural_gift_power", "size", "smoothness", "soil_dryness", "firmness", "item",
        "natural_gift_type", "flavors"
    )

    def __init__(self, data: dict):
        super().__init__(data)

        self.growth_time = data["growth_time"]
        self.max_harvest = data["max_harvest"]
        self.natural_gift_power = data["natural_gift_power"]
        self.size = data["size"]
        self.smoothness = data["smoothness"]
        self.soil_dryness = data["soil_dryness"]

        self.firmness = NamedAPIObject(data["firmness"])
        self.item = NamedAPIObject(data["item"])
        self.natural_gift_type = NamedAPIObject(data["natural_gift_type"])

        self.flavors = [BerryFlavorMap(d) for d in data["flavors"]]

    def __repr__(self) -> str:
        return "<Berry id={0.id} name='{0}'".format(self)


class BerryFlavorMap:
    """Represents a map composed of a berry flavor and his potency.

    Attributes
    ----------
    potency: :class:`int`
        How powerful the referenced flavor is for the berry.
    flavor: :class:`NamedAPIObject`
        The berry's flavor."""
    __slots__ = ("potency", "flavor")

    def __init__(self, data: dict):
        self.potency = data["potency"]
        self.flavor = NamedAPIObject(data["flavor"])

    def __repr__(self) -> str:
        return "<BerryFlavorMap potency={0.potency} flavor='{0.flavor}'>".format(self)
