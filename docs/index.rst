.. include:: ../README.rst

Developer Guide
---------------

Here is the API reference for safe.

.. module:: safe

.. autofunction:: check

.. autoclass:: Strength
   :members:

.. autofunction:: is_asdf
.. autofunction:: is_by_step
.. autofunction:: is_common_password

Changelog
----------

Here is the full history of safe.

Version 0.3
~~~~~~~~~~~

Released on Jul 28, 2014

1. API changes. Use :meth:`check` instead of safety.
2. Cache file with a version number.

Version 0.2
~~~~~~~~~~~

Released on Jul 24, 2014

1. Typo and bugfix
2. API changes in :class:`Strength`
3. Remove threading
4. Add environment variable

Version 0.1
~~~~~~~~~~~

First preview release.
