# async_pokepy
An, in the works, asynchronous wrapper for the [PokeAPI.co API](https://pokeapi.co).

## Documentation
Available available @ readthedocs soon:tm:.

## Installing
At the moment you can only install it from git with:<br>
``pip install git+github.com/PendragonLore/async_pokepy.git``

## Example
```python
import asyncio

import async_pokepy


async def main(query):
    client = await async_pokepy.Client.connect()

    pokemon = await client.get_pokemon(query)

    fmt = " ".join(map(str, pokemon.abilities))
    print("{0} has the abilities {1}".format(pokemon, fmt))

    await client.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main("Snorlax"))
```
This will output: "snorlax has the abilities gluttony thick-fat immunity"
