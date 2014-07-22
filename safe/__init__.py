# coding: utf-8
"""
    safe
    ~~~~

    Detect if your password is safe.

    :copyright: (c) 2014 by Hsiaoming Yang
"""

try:
    import cPickle as pickle
except ImportError:
    import pickle
import re
import logging
import os.path
import threading
import tempfile
from ._compat import to_unicode

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
                WORDS[name.strip()] = int(freq.strip())

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
    def __init__(self, level, message):
        self.level = level
        self.message = message

    def __repr__(self):
        if self.level < 0:
            return 'terrible'
        if self.level < 10:
            return 'simple'
        if self.level < 20:
            return 'medium'
        if self.level < 30:
            return 'strong'
        return 'unknown'

    def __nonzero__(self):
        return self.level >= 10


def safety(raw, length=6, freq=0):
    """If the password is safe."""
    raw = to_unicode(raw)

    if len(raw) < length:
        return Strength(-1, 'password is too short')

    if is_asdf(raw) or is_by_step(raw):
        return Strength(1, 'password has a pattern')

    if is_common_password(raw):
        return Strength(2, 'password is too common')

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
        return Strength(3, 'password is too simple')

    if types > 2:
        return Strength(20, 'good password')

    return Strength(10, 'usable password')
