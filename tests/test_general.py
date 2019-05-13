import asyncio
import functools
import io

import pytest

from async_pokepy import Client, NotFound, Pokemon


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

    assert isinstance(await client.get_pokemon("sNorLax"), Pokemon)
    assert isinstance(await client.get_pokemon(143), Pokemon)
    assert isinstance(await client.get_pokemon("143"), Pokemon)

    poke = await client.get_pokemon(1)

    assert isinstance(await client.read_sprite(poke.sprites.back_default), bytes)

    ret = io.BytesIO()

    assert isinstance(await client.save_sprite(poke.sprites.back_default, ret), int)

    assert client.cache_pokemon

    await client.close()

    assert not client.cache_pokemon
