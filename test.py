# coding: utf-8
import os
import tempfile

import safe

def test_asdf():
    s = safe.check('dfghjkl', length=7)
    assert not s
    assert 'pattern' in str(s)


def test_step():
    s = safe.check('abcdefg', length=7)
    assert not s
    assert 'pattern' in s.message


def test_common():
    s = safe.check('password')
    assert not s
    assert 'common' in s.message


def test_short():
    s = safe.check('1')
    assert not s
    assert 'short' in s.message


def test_simple():
    s = safe.check('yhnolku', length=6)
    assert not s
    assert 'simple' in s.message


def test_medium():
    s = safe.check('yhnolkuT', length=7)
    assert not s
    assert repr(s) == 'medium'


def test_strong():
    s = safe.check('yhnolkuT.')
    assert bool(s)
    assert 'perfect' in s.message


def test_no_cache_on_load_words():
    cache_file = _clear_cache_file()
    words = safe._load_words(cache_words=False)
    assert words
    assert not os.path.exists(cache_file)


def test_no_cache_on_safe_check():
    cache_file = _clear_cache_file()
    s = safe.check('yhnolkuT.', cache_words=False)
    assert not os.path.exists(cache_file)

def _clear_cache_file():
    filename = 'safe-%s.words.cache' % safe.__version__
    _cache_file = os.environ.get(
        'PYTHON_SAFE_WORDS_CACHE',
        os.path.join(tempfile.gettempdir(), filename),
    )
    if os.path.exists(_cache_file):
        os.remove(_cache_file)
    return _cache_file
