import asyncio
import functools
import io
import sys

import aiohttp
import pytest

from async_pokepy import Ability, Berry, Machine, Move, NamedAPIObject, NotFound, Pokemon, connect
from async_pokepy.http import Route


def run_async(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))

    return inner


@run_async
async def test_pokemon():
    client = await connect()

    assert not client.get_pokemon.cache

    with pytest.raises(NotFound):
        await client.get_pokemon("notapokemon")
        await client.get_pokemon(9999)

    assert not client.get_pokemon.cache

    poke = await client.get_pokemon(1)

    assert isinstance(poke, Pokemon)
    assert client.get_pokemon.cache

    assert not client._image_cache  # pylint: disable=protected-access
    isinstance(await client.read_sprite(poke.sprites.back_default), bytes)
    assert client._image_cache  # pylint: disable=protected-access

    ret = io.BytesIO()
    assert isinstance(await client.save_sprite(poke.sprites.back_default, ret), int)

    await client.close()


@run_async
async def test_ability():
    client = await connect()

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
    client = await connect()

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
    client = await connect()

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
    client = await connect()

    with pytest.raises(NotFound):
        await client.get_pagination("notanobj").flatten()

    assert isinstance(await client.get_pagination("pokemon").flatten(), list)
    assert isinstance(await client.get_pagination("pokemon").find(lambda x: x.id == 1), NamedAPIObject)
    assert isinstance(await client.get_pagination("pokemon").find(lambda x: x.id == 9999), type(None))
    assert isinstance(await client.get_pagination("pokemon").find_similar("bulbasaur"), list)

    await client.close()


@run_async
async def test_machine():
    client = await connect()

    assert not client.get_machine.cache

    with pytest.raises(NotFound):
        await client.get_machine("notamachine")

    assert not client.get_machine.cache

    assert isinstance(await client.get_machine(1), Machine)

    assert client.get_machine.cache

    await client.close()


@run_async
async def test_other():
    base = "https://pokeapi.co/api/v2/"

    if not sys.version_info[0:2] == (3, 5):  # unordered kwargs in py35 kinda break this
        assert Route(base, "ability", limit=20, offset=20).url == "https://pokeapi.co/api/v2/ability?limit=20&offset=20"

    assert Route(base, "pokemon").url == "https://pokeapi.co/api/v2/pokemon"
    assert Route(base, "pOkEmOn").url == "https://pokeapi.co/api/v2/pokemon"
    assert Route(base, "evoLuTioN chAin").url == "https://pokeapi.co/api/v2/evolution-chain"

    session = aiohttp.ClientSession()
    async with connect(session=session) as client:
        pokemon = await client.get_pokemon("snorlax")

        assert client._http._session is session  # pylint: disable=protected-access

    for _ in pokemon.sprites:
        pass
    assert client._http._session.closed  # pylint: disable=protected-access
