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

__version__ = '0.5'
__author__ = 'Hsiaoming Yang <me@lepture.com>'

__all__ = [
    'is_asdf', 'is_by_step', 'is_common_password',
    'check', 'Strength',
]

log = logging.getLogger('safe')

LOWER = re.compile(r'[a-z]')
UPPER = re.compile(r'[A-Z]')
NUMBER = re.compile(r'[0-9]')
MARKS = re.compile(r'[^0-9a-zA-Z]')
SYMBOL = re.compile(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]')
NUM_ASC = '01234567890'
NUM_DESC = '09876543210'

TERRIBLE = 0
SIMPLE = 1
MEDIUM = 2
STRONG = 3
VERYSTRONG = 4 


def _load_words(cache_words=True):
    if cache_words:
        filename = 'safe-%s.words.cache' % __version__
        _cache_file = os.environ.get(
            'PYTHON_SAFE_WORDS_CACHE',
            os.path.join(tempfile.gettempdir(), filename),
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
    if cache_words:
        with open(_cache_file, 'wb') as f:
            log.debug('Dump to cache file %s' % _cache_file)
            pickle.dump(words, f)
    return words

WORDS = {}
ASDF = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']


def is_asdf(raw):
    """If the password is in the order on keyboard."""

    reverse = raw[::-1]
    asdf = ''.join(ASDF)

    return raw in asdf or reverse in asdf


def is_by_step(raw):
    """If the password is alphabet step by step."""
    # make sure it is unicode
    delta = ord(raw[1]) - ord(raw[0])

    for i in range(2, len(raw)):
        if ord(raw[i]) - ord(raw[i-1]) != delta:
            return False

    return True


def is_common_password(raw, freq=0, cache_words=True):
    """If the password is common used.

    10k top passwords: https://xato.net/passwords/more-top-worst-passwords/
    """
    global WORDS
    if not WORDS:
        WORDS = _load_words(cache_words)
    frequent = WORDS.get(raw, 0)
    if freq:
        return frequent > freq
    return bool(frequent)


class Strength(object):
    """Measure the strength of a password.

    Here are some common usages of strength::

        >>> strength = Strength(True, 3, 'strong', 'password is perfect')
        >>> bool(strength)
        True
        >>> repr(strength)
        'strong'
        >>> str(strength)
        'password is perfect'

    :param valid: if the password is valid to use
    :param level: the level of the password
    :param strength: the strength level of the password
    :param message: a message related to the password
    """
    
    def __init__(self, valid, level, strength, message):
        self.valid = valid
        self.level = level
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


def check(raw, length=8, freq=0, min_types=5, min_symbol=3, min_number=3, level=STRONG, cache_words=True):
    """Check the safety level of the password.

    :param raw: raw text password.
    :param length: minimal length of the password.
    :param freq: minimum frequency.
    :param min_types: minimum character family.
    :param level: minimum level to validate a password.
    """
    raw = to_unicode(raw)
    
    if level > STRONG:
        level = STRONG

    if len(raw) < length:
        return Strength(False, TERRIBLE, 'terrible', 'password is too short').__dict__

    if is_asdf(raw) or is_by_step(raw):
        return Strength(False, SIMPLE, 'simple', 'password has a pattern').__dict__

    if is_common_password(raw, freq=freq, cache_words=cache_words):
        return Strength(False, SIMPLE, 'simple', 'password is too common').__dict__

    types = 0

    if LOWER.search(raw):
        types += 1

    if UPPER.search(raw):
        types += 1

    if NUMBER.search(raw):
        types += 1

    if MARKS.search(raw):
        types += 1
    
    if len(MARKS.findall(raw)) >= min_symbol:
        types += 2
    
    if len(NUMBER.findall(raw)) >= min_number:
        types += 2
        
    # Find all the numbe ascending
    index = 2
    while index < len(raw):
        temp_string = raw[index-2] + raw[index-1] + raw[index]
        if NUM_ASC.find(temp_string) != -1:
            types -= 1
            break
        
        index += 1

    # Find all the numbe descending
    index = 2
    while index < len(raw):
        temp_string = raw[index-2] + raw[index-1] + raw[index]
        if NUM_DESC.find(temp_string) != -1:
            types -= 1
            break
        
        index += 1  
    
    if types < 2:
        return Strength(level <= SIMPLE, SIMPLE, 'simple', 'password is too simple').__dict__

    if types < min_types:
        return Strength(level <= MEDIUM, MEDIUM, 'medium',
                        'password is good enough, but not strong').__dict__

    if types > 7:
        return Strength(True, VERYSTRONG, 'very strong', 'password is very perfect').__dict__
    return Strength(True, STRONG, 'strong', 'password is perfect').__dict__


def safety(raw, length=8, freq=0, min_types=2, level=STRONG):
    return check(raw, length=8, freq=0, min_types=2, level=STRONG)
