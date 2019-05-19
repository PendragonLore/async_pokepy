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

You can check out the (failing) pipelines @ [gitlab](https://gitlab.com/PendragonLore/async_pokepy).

## Documentation

The docs are available @ [readthedocs](https://async-pokepy.readthedocs.io/en/master/).

## Installing

The wrapper is available on PyPi, you can install it with:

``pip install async_pokepy``

If you also want to be able to run the tests/lint install it with:

``pip install async_pokepy[tests]``

For building the docs:

``pip install async_pokepy[docs]``

## Example

```python
import asyncio

import async_pokepy


async def main(query):
    client = await async_pokepy.Client.connect()

    pokemon = await client.get_pokemon(query)

    fmt = ", ".join(map(str, pokemon.abilities))
    print("{0} has the abilities {1}".format(pokemon, fmt))

    await client.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main("Snorlax"))
```

This will output: "Snorlax has the abilities Gluttony, Thick Fat, Immunity".

You can check out more examples in the [example](https://github.com/PendragonLore/async_pokepy/tree/master/example)
folder in the github repository or in the introduction section of the docs.
