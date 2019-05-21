# ![Logo](https://i.imgur.com/HbPBYwf.png) async_pokepy

[![PyPI pyversions](https://img.shields.io/pypi/pyversions/async_pokepy.svg)](https://pypi.python.org/pypi/async-pokepy/)
[![PyPI status](https://img.shields.io/pypi/status/async_pokepy.svg)](https://pypi.python.org/pypi/async_pokepy/)
[![PyPI license](https://img.shields.io/pypi/l/async_pokepy.svg)](https://github.com/PendragonLore/async_pokepy/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/async-pokepy/badge/?version=master)](https://async-pokepy.readthedocs.io/en/master/?badge=master)
[![Pipelines Status](https://gitlab.com/PendragonLore/async_pokepy/badges/master/pipeline.svg)](https://gitlab.com/PendragonLore/async_pokepy/pipelines)
[![Build Status](https://img.shields.io/travis/com/PendragonLore/async_pokepy.svg?label=TravisCI)](https://travis-ci.com/PendragonLore/async_pokepy)
[![CircleCI](https://img.shields.io/circleci/project/github/PendragonLore/async_pokepy/master.svg?label=CircleCI)](https://circleci.com/gh/PendragonLore/async_pokepy)
[![AppYevorCI](https://img.shields.io/appveyor/ci/PendragonLore/async-pokepy/master.svg?label=AppVeyorCI)](https://ci.appveyor.com/project/PendragonLore/async-pokepy)

An, in the works, asynchronous wrapper for the [PokeAPI.co API](https://pokeapi.co).

## Documentation

The documentation is available at [readthedocs](https://async-pokepy.readthedocs.io/en/master/) or on
[gitlab pages](https://pendragonlore.gitlab.io/async_pokepy/), mostly as a backup.

## Installing

The wrapper is available on PyPi and requires Python 3.5.3+, to install it just run the following command:

```sh
python3 -m pip install -U async_pokepy

# or on Windows
py -3 -m pip install -U async_pokepy
```

To install the development version, do the this instead:

```sh
git clone https://github.com/PendragonLore/async_pokepy.git
cd async_pokepy
python3 -m pip install -U .
```

### Better caching

It's recommended to install the library with [lru-dict](https://pypi.org/project/lru-dict/), to do so, run the follwing command:

``pip install async_pokepy[lru]``

A warning will be thrown if the wrapper is used without this extra package.

### Documentation building, linting and tests

To run tests/lint install it with:

``pip install async_pokepy[tests]``

The best way to run tests is by using ``tox``.

For documentation building:

``pip install async_pokepy[docs]``

## Example

```python
import asyncio

import async_pokepy


async def main(query):
    client = await async_pokepy.connect()

    pokemon = await client.get_pokemon(query)

    fmt = ", ".join(map(str, pokemon.abilities))
    print("{0} has the abilities {1}".format(pokemon, fmt))

    await client.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main("Snorlax"))
```

This will output: "Snorlax has the abilities Gluttony, Thick Fat, Immunity".

More examples are available in the [example](https://github.com/PendragonLore/async_pokepy/tree/master/example)
folder in the github repository or in the [introduction section of the docs](https://async-pokepy.readthedocs.io/en/master/introduction.html).
