import asyncio

import async_pokepy


async def main():
    client = await async_pokepy.connect()

    # Ask for input
    name = input("What Pokémon do you want to search? ")

    try:
        result = await client.get_pokemon(name)
    except async_pokepy.NotFound:
        # No Pokémon was immediatly found, let's try a fuzzy search
        fuzzy = await client.get_pagination("pokemon", limit=800).find_similar(name)

        if not fuzzy:
            print("No Pokémon found by name {0}.".format(name))
        else:
            result = fuzzy[0]  #  The first result is always the most accurate
            print("No Pokémon found by name {0}, did you mean {1}?".format(name, result))
    else:
        print("Found {0} which has {1} abilities and {2} moves!"
              .format(result, len(result.abilities), len(result.moves)))
    finally:
        # Cleanup properly.
        await client.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
