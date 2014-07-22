# coding: utf-8
"""
    safe._compat

    Compatible module for Python 2 and Python 3.

    :copyright: (c) 2014 by Hsiaoming Yang
"""


import sys

if sys.version_info[0] == 3:
    unicode_type = str
    bytes_type = bytes
else:
    unicode_type = unicode
    bytes_type = str


def to_unicode(value, encoding='utf-8'):
    if isinstance(value, unicode_type):
        return value

    if isinstance(value, bytes_type):
        return unicode_type(value, encoding=encoding)

    if isinstance(value, int):
        return unicode_type(str(value))

    return value
