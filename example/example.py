import asyncio

import async_pokepy


<<<<<<< HEAD
async def main(query):
    client = await async_pokepy.Client.connect()

    pokemon = await client.get_pokemon(query)

    fmt = " ".join(map(str, pokemon.abilities))
    print("{0} has the abilities {1}".format(pokemon, fmt))
=======
async def main(loop, query):
    client = await async_pokepy.Client.connect(loop=loop)

    pokemon = await client.get_pokemon(query)
    abilities = ", ".join(pokemon.abilities)
    print("{0} has the abilities {1}!".format(pokemon, abilities))
>>>>>>> f50dd6de53c3b96a32607eebc0c8fc280173f502

    await client.close()


loop = asyncio.get_event_loop()
<<<<<<< HEAD
loop.run_until_complete(main("Snorlax"))

# This will output: "snorlax has the abilities gluttony thick-fat immunity"
=======
loop.run_until_complete(main(loop, "Snorlax"))

# This will output: "Snorlax has the abilities Immunity, Thick fat, Gluttony!"
>>>>>>> f50dd6de53c3b96a32607eebc0c8fc280173f502
