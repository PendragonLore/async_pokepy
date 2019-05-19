import asyncio
import functools
import io

import pytest

from async_pokepy import Ability, Berry, Client, Move, NamedAPIObject, NotFound, Pokemon


def run_async(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))

    return inner


@run_async
async def test_pokemon():
    client = await Client.connect()

    assert not client.get_pokemon.cache

    with pytest.raises(NotFound):
        await client.get_pokemon("notapokemon")
        await client.get_pokemon(9999)

    assert not client.get_pokemon.cache

    poke = await client.get_pokemon(1)

    assert isinstance(poke, Pokemon)
    assert client.get_pokemon.cache

    assert not client._image_cache
    isinstance(await client.read_sprite(poke.sprites.back_default), bytes)
    assert client._image_cache

    ret = io.BytesIO()
    assert isinstance(await client.save_sprite(poke.sprites.back_default, ret), int)

    await client.close()


@run_async
async def test_ability():
    client = await Client.connect()

    assert not client.get_ability.cache

    with pytest.raises(NotFound):
        await client.get_ability("notanability")
        await client.get_ability(9999)

    assert not client.get_ability.cache

    ability = await client.get_ability(1)

    assert isinstance(ability, Ability)
    assert client.get_ability.cache

    await client.close()


@run_async
async def test_move():
    client = await Client.connect()

    assert not client.get_move.cache

    with pytest.raises(NotFound):
        await client.get_move("notamove")
        await client.get_move(99999)

    assert not client.get_move.cache

    move = await client.get_move(1)

    assert isinstance(move, Move)
    assert client.get_move.cache

    await client.close()


@run_async
async def test_berry():
    client = await Client.connect()

    assert not client.get_berry.cache

    with pytest.raises(NotFound):
        await client.get_berry("getberry")
        await client.get_berry(99999)

    assert not client.get_berry.cache

    berry = await client.get_berry(1)

    assert isinstance(berry, Berry)
    assert client.get_berry.cache

    await client.close()


@run_async
async def test_pagination():
    client = await Client.connect()

    with pytest.raises(NotFound):
        await client.get_pagination("notanobj").flatten()

    assert isinstance(await client.get_pagination("pokemon").flatten(), list)
    assert isinstance(await client.get_pagination("pokemon").find(lambda x: x.id == 1), NamedAPIObject)
    assert isinstance(await client.get_pagination("pokemon").find(lambda x: x.id == 9999), type(None))

    await client.close()
