# coding: utf-8

import safe


def test_asdf():
    s = safe.check('dfghjkl')
    assert not s
    assert 'pattern' in str(s)


def test_step():
    s = safe.check('abcdefg')
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
    s = safe.check('yhnolku')
    assert s
    assert 'simple' in s.message


def test_medium():
    s = safe.check('yhnolkuT')
    assert s
    assert repr(s) == 'medium'


def test_strong():
    s = safe.check('yhnolkuT.')
    assert bool(s)
    assert 'perfect' in s.message
