# -*- coding: utf-8 -*-

"""
PokeAPI.co API Wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper for the PokeAPI.co API.
:copyright: (c) 2019 Lorenzo
:license: MIT, see LICENSE for more details.
"""

__title__ = "async_pokepy"
__author__ = "Lorenzo"
__docformat__ = "restructuredtext en"
__license__ = "MIT"
__copyright__ = "Copyright 2019 Lorenzo"
__version__ = "0.1.6a"

from collections import namedtuple

from .client import Client, connect  # noqa: F401
from .exceptions import *  # noqa: F401
from .types import *  # noqa: F401

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel")

version_info = VersionInfo(major=0, minor=1, micro=6, releaselevel="alpha")
