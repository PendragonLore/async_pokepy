.. currentmodule:: async_pokepy

Changelog
=========

This page aims to keep an organized view of all of the changes
since the wrapper's initial release.


0.1.1a
------

- Sprites from :meth:`Client.read_sprite` and :meth:`Client.save_sprite`
  are now cached.
- Slight improvements in internal caching.

0.1.0a
------

- :class:`Move` objects and :meth:`Client.get_move`
  (still incomplete and need testing).
- Integrated :class:`AsyncIterator` and :meth:`Client.get_pagination`
  for API pagination, still incomplete and needs testing too.
- :data:`version_info` for a :data:`sys.version_info`-like
  :class:`~collections.namedtuple`.
- All modules now have ``__all__`` defined to them.

0.0.9a
------

- :meth:`Client.read_sprite` and :meth:`Client.save_sprite`
  for easy sprite downloading.
- Base URI to make requests to and the User-Agent header are now customizable.
- Pretty formatted names, e.g ``thick-fat`` is now ``Thick Fat``.
- Full objects are now searchable by both name and id.
- Improvements in internal routing.

0.0.7a
------

- First release.
