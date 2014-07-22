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
import threading
import tempfile
from ._compat import to_unicode, pickle

__version__ = '0.1'
__author__ = 'Hsiaoming Yang <me@lepture.com>'

__all__ = [
    'is_asdf', 'is_by_step', 'is_common_password',
    'safety', 'Strength',
]

log = logging.getLogger('safe')

WORD_LOCK = threading.RLock()
WORDS = {}

LOWER = re.compile(r'[a-z]')
UPPER = re.compile(r'[A-Z]')
NUMBER = re.compile(r'[0-9]')
MARKS = re.compile(r'[^0-9a-zA-Z]')


def _init_words():
    global WORDS
    with WORD_LOCK:
        if WORDS:
            return

        cache_file = os.path.join(
            tempfile.gettempdir(),
            'password.words.cache'
        )

        if os.path.exists(cache_file):
            log.debug('Reading from cache file %s' % cache_file)
            try:
                with open(cache_file, 'rb') as f:
                    WORDS = pickle.load(f)
                    return
            except:
                pass

        libdir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(libdir, 'words.dat')
        with open(filepath, 'rb') as f:
            for line in f.readlines():
                name, freq = line.split()
                WORDS[to_unicode(name.strip())] = int(freq.strip())

        with open(cache_file, 'wb') as f:
            log.debug('Dump to cache file %s' % cache_file)
            pickle.dump(WORDS, f)


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
    _init_words()
    frequent = WORDS.get(raw, 0)
    if freq:
        return frequent > freq
    return bool(frequent)


class Strength(object):
    """Measure the strength of a password."""
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


def safety(raw, length=6, freq=0):
    """Check the safety level of the password.

    :param raw: raw text password.
    :param length: minimal length of the password.
    """
    raw = to_unicode(raw)

    if len(raw) < length:
        return Strength(False, 'terrible', 'password is too short')

    if is_asdf(raw) or is_by_step(raw):
        return Strength(False, 'simple', 'password has a pattern')

    if is_common_password(raw):
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
