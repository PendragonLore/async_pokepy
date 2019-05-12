.. py:currentmodule:: async_pokepy

API reference
=============
This section of the documentation outlines ``async_pokepy``'s API.

Version Related Info
--------------------
.. data:: __version__

    A string representation of the version. e.g. ``'1.0.0rc1'``. This is based
    off of `PEP-440 <https://www.python.org/dev/peps/pep-0440/>`_.

Client
------
.. autoclass:: Client()
    :members:


.. _ABCs:

Abstract base class
-------------------
An abstract base class (also known as an :class:`~abc.ABC`) is a class that
models can inherit to get their behaviour.

**Abstract base classes cannot be instantiated.**

.. autoclass:: BaseObject()
    :members:
    :inherited-members:

Data Classes
------------

Data classes all representing an API object, most of them just store data.

.. danger::

    Just like :ref:`ABCs <ABCs>` these classes are **not** meant to be initiated by users.

.. note::

    All data classes here have :ref:`__slots__ <python:slots>`
    defined which means that it is impossible to have dynamic attributes to them.

Pokemon
^^^^^^^

.. autoclass:: Pokemon()
    :members:
    :inherited-members:

.. autoclass:: PokemonMove()
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

Version
^^^^^^^

.. autoclass:: PokemonMoveVersion()
    :members:

.. autoclass:: PokemonHeldItemVersion()
    :members:

.. autoclass:: VersionGameIndex()
    :members:


Exceptions
----------

.. autoexception:: PokemonException()

.. autoexception:: PokeAPIException()

.. autoexception:: NotFound()

.. autoexception:: Forbidden()

.. autoexception:: RateLimited()
