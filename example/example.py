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

# This will output: "Snorlax has the abilities Gluttony, Thick Fat, immunity"
