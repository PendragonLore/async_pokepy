import asyncio
import pytest
import functools

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
    assert client._cache_pokemon

    await client.close()

    assert not client._cache_pokemon
