import asyncio
import functools
import io

import pytest

from async_pokepy import Ability, Client, Move, NotFound, Pokemon


def run_async(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))

    return inner


@run_async
async def test_general():
    client = await Client.connect()

    assert isinstance(client.loop, asyncio.AbstractEventLoop)

    with pytest.raises(NotFound):
        await client.get_pokemon("notapokemon")
        await client.get_move("notamove")
        await client.get_ability("notanability")

    assert isinstance(await client.get_pokemon("sNorLax"), Pokemon)
    assert isinstance(await client.get_pokemon(143), Pokemon)
    assert isinstance(await client.get_pokemon("143"), Pokemon)

    poke = await client.get_pokemon(1)

    assert isinstance(await client.read_sprite(poke.sprites.back_default), bytes)

    ret = io.BytesIO()

    assert isinstance(await client.save_sprite(poke.sprites.back_default, ret), int)

    assert client.get_pokemon.cache

    assert isinstance(await client.get_move(1), Move)

    async for _ in client.get_pagination("pokemon", limit=20, offset=0):
        pass

    assert isinstance(await client.get_pagination("pokemon", limit=20, offset=50).flatten(), list)
    assert isinstance(await client.get_pagination("pokemon", limit=150, offset=0).find_similar("snorlax"), list)
    assert isinstance(await client.get_pagination("pokemon", limit=1, offset=0).find(lambda i: i[1] == 1), tuple)
    assert client.get_move.cache

    assert isinstance(await client.get_ability(1), Ability)
    assert client.get_ability.cache

    await client.close()
