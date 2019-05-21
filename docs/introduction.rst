.. currentmodule:: async_pokepy

Introduction
============

Installing
----------

The wrapper **requires** Python 3.5.3.

Since the library is available on `PyPi <https://pypi.org/project/async-pokepy/>`_
it is really easy to install by running this command:

.. code-block:: sh

    python3 -m pip install -U async_pokepy

    # or on Windows
    py -3 -m pip install -U async_pokepy

It's also very much recommended to install it with lru-dict
for faster, more memory efficient caching; which is easy to do
through the following command:

.. code-block:: sh

    python3 -m pip install -U async_pokepy[lru]

    # or on Windows
    py -3 -m pip install -U async_pokepy[lru]

Examples
--------

This wrapper was specifically made to be
simple, fast, ready and easy to use.

In this part of the documentation you will find
some basic examples on how to use this library.

Basic example
~~~~~~~~~~~~~

This is a basic example that shows how the library is structured.

This also uses the `ipython interpreter <https://ipython.org>`_ due
to the easier and better looking execution of asynchronous code.

.. code-block:: python3

    # First we import the library.
    In [1]: import async_pokepy

    # Then we initiate a client through the connect method.
    # It's a good practice to only have a single client
    # and to close it when done.
    In [2]: client = await async_pokepy.connect()

    # Let's search for a Pokémon! Let's say, Snorlax.
    In [3]: pokemon = await client.get_pokemon("snorlax")

    # By printing the Pokémon we can get it's name.
    In [4]: print(pokemon)
    Out[4]: Snorlax

    # Or the repr, which also contains the ID.
    In [5]: pokemon
    Out[5]: <Pokemon id=143 name='Snorlax'>

    # Can also get them by ID.
    In [6]: await client.get_pokemon(1)
    Out[6]: <Pokemon id=1 name='Bulbasaur'>

    # ID as a string too
    # This will also be much faster due to caching
    In [7]: await client.get_pokemon("1")
    Out[7]: <Pokemon id=1 name='Bulbasaur'>

    # Trying to search for a pokemon not present in the API
    # will raise an error.
    In [8]: await client.get_pokemon("notapokemon")
    Out[8]: NotFound: API responded with status code 404 Not Found: Endpoint not found.

    # Now let's try to print Snorlax's abilities.
    # Pokemon.abilities is a list of PokemonAbility the Pokémon can have.
    # PokemonAbility can be stringfied to obtain the name of the ability.
    # Let's try it then.
    In [9]: list(map(str, pokemon.abilities))  # Could also be a list comp
    Out[9]: ['Gluttony', 'Thick Fat', 'Immunity']

    # Also, capitalization doesn't matter.
    In [10]: await client.get_pokemon("pIkaChu")
    Out[10]: <Pokemon id=25 name='Pikachu'>

    # Finally, let's close the client.
    In [11]: await client.close()

This is the basic gist of the library,
but let's try with something more concrete.

Fuzzy user input based search
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python3

    import asyncio

    import async_pokepy


    async def main():
        client = await async_pokepy.Client.connect()

        # Ask for input
        name = input("What Pokémon do you want to search? ")

        try:
            result = await client.get_pokemon(name)
        except async_pokepy.NotFound:
            # No Pokémon was immediatly found, let's try a fuzzy search.
            fuzzy = await client.get_pagination("pokemon", limit=800).find_similar(name)

            if not fuzzy:
                print("No Pokémon found by name {0}.".format(name))
            else:
                result = fuzzy[0]  #  The first result is always the most accurate.
                print("No Pokémon found by name {0}, did you mean {1}?".format(name, result))
        else:
            print("Found {0} which has {1} abilities and {2} moves!"
                .format(result, len(result.abilities), len(result.moves)))
        finally:
            # Cleanup properly.
            await client.close()


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


This simple example demonstrates how to use
:meth:`Client.get_pagination` for a simple fuzzy search.
