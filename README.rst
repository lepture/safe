Safe
====

Is your password safe? **Safe** will check the password strength for you.

.. image:: https://travis-ci.org/lepture/safe.png?branch=master
   :target: https://travis-ci.org/lepture/safe


Installation
------------

Install Safe with pip::

    $ pip install Safe

If pip is not available, try easy_install::

    $ easy_install Safe

Usage
-----

It's very simple to check the strength of a password::

    >>> import safe
    >>> safe.safety(1)
    terrible
    >>> safe.safety('password')
    simpile
    >>> safe.safety('is.safe')
    medium
    >>> safe.safety('x*V-92Ba')
    strong
    >>> strength = safe.safety('x*V-92Ba')
    >>> bool(strength)
    True
    >>> s.level
    20
    >>> s.message
    'good password'
