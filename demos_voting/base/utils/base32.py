# File: base32.py

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import random as _random
import re

from demos_voting.base.utils.compatibility import int_from_bytes, int_to_bytes
from django.utils.six.moves import zip_longest

# Reference: http://www.crockford.com/wrmg/base32.html


symbols = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
regex = r'(?!-)(-?[0-9A-TV-Za-tv-z])'


def encode(number, length=0, hyphens=0):
    """
    Encodes an integer to a Crockford's Base32 string. 'number' is the integer
    to encode, if 'length' > 0 the resulting encoded string is padded on the
    left with '0' digits until the given length is reached, if 'hyphens' > 0
    a hyphen is added every n characters. The encoded string is returned.
    """

    if number < 0:
        raise ValueError("'%d' is not a non-negative integer" % number)

    encoded = ''

    while number:

        d = number >> 5
        m = number - (d << 5)

        encoded = symbols[m] + encoded
        number = d

    if length > 0:
        encoded = encoded.zfill(length)

    if hyphens > 0:
        encoded = _hyphen(encoded, hyphens)

    return encoded or '0'


def encode_from_bytes(bytes, *args, **kwargs):

    number = int_from_bytes(bytes, 'big')
    return encode(number, *args, **kwargs)


def decode(encoded):
    """
    Decodes a Crockford's Base32 encoded string. 'encoded' is the string to
    decode. The resulting integer is returned.
    """

    _raise_for_invalid(encoded)
    encoded = _normalize(encoded)

    number = 0
    for c in encoded:
        number = symbols.index(c) + (number << 5)

    return number


def decode_to_bytes(encoded, numbytes=0, *args, **kwargs):

    number = decode(encoded, *args, **kwargs)
    return int_to_bytes(number, max([numbytes, (number.bit_length() + 7) // 8]), 'big')


_validation_regex = re.compile(r'^%s+$' % regex)

def _raise_for_invalid(encoded):
    if not _validation_regex.match(encoded):
        raise ValueError("'%s' is not a valid base32 string" % encoded)


try:
    _normalization_table = str.maketrans('OIL', '011', '-')
except AttributeError:
    _normalization_table = {ord(x): ord(y) if y else None for x, y in zip_longest('OIL-', '011')}

def _normalize(encoded):
    return encoded.upper().translate(_normalization_table)


def normalize(encoded):
    """
    Normalizes a Crockford's Base32 encoded string by removing all hyphens,
    converting all characters to upper-case and replacing 'I', 'L' with '1'
    and 'O' with '0'.
    """

    _raise_for_invalid(encoded)
    return _normalize(encoded)


def _hyphen(encoded, hyphens):

    if hyphens >= 0:
        encoded = encoded.replace('-', '')

    if hyphens > 0:
        encoded = '-'.join(re.findall('.{,%s}' % hyphens, encoded)[:-1])

    return encoded


def hyphen(encoded, hyphens):
    """
    Manages hyphens in a Crockford's Base32 string. 'hyphens' controls how
    hyphens are treated, 0 removes all hyphens, n > 0 adds a hyphen every
    'n' characters.
    """

    _raise_for_invalid(encoded)
    return _hyphen(encoded, hyphens)


def random(length, hyphens=0, urandom=False):
    """
    Generates a random Crockford's Base32 encoded string. 'length' is the
    length of resulting encoded string, if 'hyphens' > 0 an hyphen is added
    every 'n' characters, 'urandom' selects whether os.urandom or a pseudo
    random number generator will be used.
    """

    random = _random

    if urandom:
        random = random.SystemRandom()

    number = random.getrandbits(length * 5)
    return encode(number, length, hyphens)
