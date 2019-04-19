import asyncio

import async_pokepy


async def main(loop, query):
    client = await async_pokepy.Client.connect(loop=loop)

    pokemon = await client.get_pokemon(query)
    abilities = ", ".join(pokemon.abilities)
    print("{0} has the abilities {1}!".format(pokemon, abilities))

    await client.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop, "Snorlax"))

# This will output: "Snorlax has the abilities Immunity, Thick fat, Gluttony!"
