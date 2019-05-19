.. py:currentmodule:: async_pokepy

API reference
=============
This section of the documentation outlines ``async_pokepy``'s API.

Version Related Info
--------------------

.. data:: __version__

    A string representation of the version. e.g. ``'1.0.0rc1'``. This is based
    off of `PEP-440 <https://www.python.org/dev/peps/pep-0440/>`_.

.. data:: version_info

    A :func:`collections.namedtuple` that is similar to :data:`sys.version_info`.

    Just like :data:`sys.version_info` the valid values for releaselevel are
    ‘alpha’, ‘beta’, ‘candidate’ and ‘final’.

Client
------

.. autoclass:: Client()
    :members:


.. _ABCs:

Abstract base classes
---------------------

An abstract base class (also known as an :class:`~abc.ABC`) is a class that
models can inherit to get their behaviour.

**Abstract base classes cannot be instantiated.**

.. autoclass:: BaseObject()
    :members:
    :inherited-members:

.. autoclass:: AsyncIterator()
    :members:

Data Classes
------------

Data classes all representing an API object, most of them just store data.

.. danger::

    Just like :ref:`ABCs <ABCs>` these classes are **not** meant to be initiated by users.

.. note::

    All data classes here have :ref:`__slots__ <python:slots>`
    defined which means that it is impossible to have dynamic attributes to them.

Pokemon
~~~~~~~

.. autoclass:: Pokemon()
    :members:
    :inherited-members:

.. autoclass:: PokemonMove()
    :members:

.. autoclass:: PokemonMoveVersion()
    :members:

.. autoclass:: PokemonAbility()
    :members:

.. autoclass:: PokemonStat()
    :members:

.. autoclass:: PokemonType()
    :members:

.. autoclass:: PokemonSprites()
    :members:

.. autoclass:: PokemonHeldItem()
    :members:

.. autoclass:: PokemonHeldItemVersion()
    :members:

Move
~~~~

.. autoclass:: Move()
    :members:
    :inherited-members:

.. autoclass:: MoveFlavorText()
    :members:

.. autoclass:: MoveMetaData()
    :members:

.. autoclass:: PastMoveStatValues()
    :members:

.. autoclass:: ContestComboDetail()
    :members:

.. autoclass:: ContestComboSet()
    :members:

Ability
~~~~~~~

.. autoclass:: Ability()
    :members:
    :inherited-members:

.. autoclass:: AbilityPokemon()
    :members:

.. autoclass:: AbilityEffectChange()
    :members:

.. autoclass:: AbilityPokemon()
    :members:

.. autoclass:: AbilityFlavorText()
    :members:

Berry
~~~~~

.. autoclass:: Berry()
    :members:
    :inherited-members:

.. autoclass:: BerryFlavorMap()
    :members:

Common
~~~~~~

Some common data classes used by the API.

.. autoclass:: APIObject()
    :members:

.. autoclass:: NamedAPIObject()
    :members:

.. autoclass:: Name()
    :members:

.. autoclass:: Effect()
    :members:

.. autoclass:: VerboseEffect()
    :members:

.. autoclass:: VersionGameIndex()
    :members:

Iterators
~~~~~~~~~

.. autoclass:: AsyncPaginationIterator()
    :members:
    :inherited-members:

Exceptions
----------

.. autoexception:: PokemonException()

.. autoexception:: PokeAPIException()

.. autoexception:: NotFound()

.. autoexception:: Forbidden()

.. autoexception:: RateLimited()

.. autoexception:: NoMoreItems()
