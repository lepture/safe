# coding: utf-8
"""
    safe
    ~~~~

    Detect if your password is safe.

    :copyright: (c) 2014 by Hsiaoming Yang
"""

import re
import logging
import os.path
import tempfile
from ._compat import to_unicode, pickle

__version__ = '0.2'
__author__ = 'Hsiaoming Yang <me@lepture.com>'

__all__ = [
    'is_asdf', 'is_by_step', 'is_common_password',
    'safety', 'Strength',
]

log = logging.getLogger('safe')

LOWER = re.compile(r'[a-z]')
UPPER = re.compile(r'[A-Z]')
NUMBER = re.compile(r'[0-9]')
MARKS = re.compile(r'[^0-9a-zA-Z]')


def _load_words():
    _cache_file = os.environ.get(
        'PYTHON_SAFE_WORDS_CACHE',
        os.path.join(tempfile.gettempdir(), 'password.words.cache'),
    )

    if os.path.exists(_cache_file):
        log.debug('Reading from cache file %s' % _cache_file)
        try:
            with open(_cache_file, 'rb') as f:
                return pickle.load(f)
        except:
            pass

    filepath = os.environ.get(
        'PYTHON_SAFE_WORDS_FILE',
        os.path.join(os.path.dirname(__file__), 'words.dat'),
    )
    words = {}
    with open(filepath, 'rb') as f:
        for line in f.readlines():
            name, freq = line.split()
            words[to_unicode(name.strip())] = int(freq.strip())

    with open(_cache_file, 'wb') as f:
        log.debug('Dump to cache file %s' % _cache_file)
        pickle.dump(words, f)
    return words

WORDS = _load_words()
ASDF = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']


def is_asdf(raw):
    """If the password is in the order on keyboard."""

    reverse = raw[::-1]
    asdf = ''.join(ASDF)

    if raw in asdf or reverse in asdf:
        return True

    asdf = ''.join(ASDF[::-1])

    return raw in asdf or reverse in asdf


def is_by_step(raw):
    """If the password is alphabet step by step."""
    # make sure it is unicode
    delta = ord(raw[1]) - ord(raw[0])

    for i in range(2, len(raw)):
        if ord(raw[i]) - ord(raw[i-1]) != delta:
            return False

    return True


def is_common_password(raw, freq=0):
    """If the password is common used.

    10k top passwords: https://xato.net/passwords/more-top-worst-passwords/
    """
    frequent = WORDS.get(raw, 0)
    if freq:
        return frequent > freq
    return bool(frequent)


class Strength(object):
    """Measure the strength of a password.

    Here are some common usages of strength::

        >>> strength = Strength(True, 'strong', 'password is perfect')
        >>> bool(strength)
        True
        >>> repr(strength)
        'strong'
        >>> str(strength)
        'password is perfect'

    :param valid: if the password is valid to use
    :param strength: the strength level of the password
    :param message: a message related to the password
    """
    def __init__(self, valid, strength, message):
        self.valid = valid
        self.strength = strength
        self.message = message

    def __repr__(self):
        return self.strength

    def __str__(self):
        return self.message

    def __unicode__(self):
        return self.message

    def __nonzero__(self):
        return self.valid

    def __bool__(self):
        return self.valid


def safety(raw, length=4, freq=0):
    """Check the safety level of the password.

    :param raw: raw text password.
    :param length: minimal length of the password.
    """
    raw = to_unicode(raw)

    if len(raw) < length:
        return Strength(False, 'terrible', 'password is too short')

    if is_asdf(raw) or is_by_step(raw):
        return Strength(False, 'simple', 'password has a pattern')

    if is_common_password(raw, freq=freq):
        return Strength(False, 'simple', 'password is too common')

    types = 0

    if LOWER.search(raw):
        types += 1

    if UPPER.search(raw):
        types += 1

    if NUMBER.search(raw):
        types += 1

    if MARKS.search(raw):
        types += 1

    if len(raw) < 8 and types < 2:
        return Strength(True, 'simple', 'password is too simple')

    if types > 2:
        return Strength(True, 'strong', 'password is perfect')

    return Strength(True, 'medium', 'password is good enough')
