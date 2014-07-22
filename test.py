# coding: utf-8

import safe


def test_asdf():
    s = safe.safety('dfghjkl')
    assert not s
    assert 'pattern' in s.message


def test_step():
    s = safe.safety('abcdefg')
    assert not s
    assert 'pattern' in s.message


def test_common():
    s = safe.safety('password')
    assert not s
    assert 'common' in s.message


def test_short():
    s = safe.safety('1')
    assert not s
    assert 'short' in s.message


def test_simple():
    s = safe.safety('yhnolku')
    assert not s
    assert 'simple' in s.message


def test_medium():
    s = safe.safety('yhnolkuT')
    assert s
    assert repr(s) == 'medium'


def test_strong():
    s = safe.safety('yhnolkuT.')
    assert s
    assert 'perfect' in s.message
