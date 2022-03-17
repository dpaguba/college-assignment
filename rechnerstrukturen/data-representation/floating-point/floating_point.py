"""IEEE 754 single precision: sign, exponent, significand.

Thirty-two bits split one, eight and twenty-three. The exponent is stored in
excess by 127, which makes the encoded form compare like an integer, and the
significand has an implicit leading one, which buys a free bit of precision.

The consequences are what the exercises ask about. Numbers are spaced
logarithmically, so the gap between representable values doubles with every
exponent. Addition is not associative. Almost no decimal fraction is exact.
"""

from __future__ import annotations

import math
import struct


def encode(value):
    """The 32-bit pattern of a float."""
    packed = struct.unpack(">I", struct.pack(">f", value))[0]
    return format(packed, "032b")


def decode(pattern):
    """The float a 32-bit pattern denotes."""
    return struct.unpack(">f", struct.pack(">I", int(pattern, 2)))[0]


def fields(pattern):
    """The three fields, as integers."""
    return {"sign": int(pattern[0], 2),
            "exponent": int(pattern[1:9], 2),
            "significand": int(pattern[9:], 2)}


def classify(pattern):
    """Which of the five categories a pattern falls into.

    The exponent field decides: all zeros means zero or a denormal, all ones
    means infinity or a NaN, and everything between is a normal number. Those
    two reserved patterns are why the exponent range is 1 to 254 rather than 0
    to 255.
    """
    parts = fields(pattern)

    if parts["exponent"] == 0:
        return "zero" if parts["significand"] == 0 else "denormal"
    if parts["exponent"] == 255:
        return "infinity" if parts["significand"] == 0 else "nan"
    return "normal"


def is_denormal(pattern):
    """Whether a pattern is a denormal number.

    Denormals fill the gap between zero and the smallest normal number, which
    would otherwise be much larger than the gap between the two smallest
    normals. They cost precision and, on many processors, a large amount of
    time.
    """
    return classify(pattern) == "denormal"


def spacing_at(value):
    """The distance to the next representable number.

    Doubles at every power of two, which is the whole point of a floating
    representation: the relative error is roughly constant and the absolute
    error is not. At 1.0 the spacing is about 1.2e-07 and at 1024 it is about
    1.2e-04.
    """
    return math.ulp(struct.unpack(">f", struct.pack(">f", value))[0])


def add32(left, right):
    """Add two numbers with single-precision rounding after the operation."""
    return decode(encode(left + right))


def is_exact(value):
    """Whether a value survives a round trip through the encoding."""
    return decode(encode(value)) == value


def representable_near(value, count=3):
    """The neighbouring representable numbers, for showing the spacing."""
    packed = struct.unpack(">I", struct.pack(">f", value))[0]
    return [decode(format(packed + offset, "032b"))
            for offset in range(-count, count + 1)]


def associativity_witness():
    """A triple where floating addition is not associative.

    `(1e10 + -1e10) + 1` is 1, and `1e10 + (-1e10 + 1)` is 0, because the 1 is
    lost when added to 1e10. The two orders differ by the whole value, and no
    amount of precision removes the phenomenon: it moves the threshold.
    """
    left = add32(add32(1e10, -1e10), 1.0)
    right = add32(1e10, add32(-1e10, 1.0))
    return {"left": left, "right": right, "equal": left == right}
