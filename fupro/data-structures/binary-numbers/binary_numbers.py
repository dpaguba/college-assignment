"""The exam's binary numbers, with the fold it asks to define first.

```haskell
data Bin = LSB | Zero Bin | One Bin
```

The marker sits innermost, so the constructor closest to it carries the
lowest place value: ``One (Zero LSB)`` is 2 and ``One LSB`` is 1. Getting the
direction backwards is the easiest way to fail the whole exercise, and every
function here is checked against the four examples the exam prints.

Once the fold exists, doubling is one line, because a shift is exactly the
fold that reassembles the number with a zero bit added at the bottom.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "haskell-core", "algebraic-data-types"))
import algebraic_data_types as adt

LSB = adt.construct("LSB")
"""The marker at the least significant end."""


def zero(rest):
    """A zero bit above the given number."""
    return adt.construct("Zero", rest)


def one(rest):
    """A one bit above the given number."""
    return adt.construct("One", rest)


def fold_b(marker, on_zero, on_one, value):
    """The fold of the type, with one value or function per constructor.

    The signature the exam prescribes. It replaces the constructors from the
    outside in, so ``on_one`` is applied to the result of folding what is
    below it, and the traversal direction is the same as the reading
    direction of the number.
    """
    name = adt.name_of(value)
    if name == "LSB":
        return marker
    inner = fold_b(marker, on_zero, on_one, adt.arguments_of(value)[0])
    return on_zero(inner) if name == "Zero" else on_one(inner)


def value(number):
    """The natural number a term stands for.

    The fold carries a pair, the value so far and the place value of the next
    bit, because the traversal reaches the least significant bit first. The
    obvious fold that only doubles reads the term in the opposite direction
    and computes the value of the reversed bit string: on the term for 13 it
    returns 11.
    """
    total, _weight = fold_b((0, 1),
                            lambda pair: (pair[0], pair[1] * 2),
                            lambda pair: (pair[0] + pair[1], pair[1] * 2),
                            number)
    return total


def reversed_value(number):
    """What the naive doubling fold computes, which is the bit reversal."""
    return fold_b(0, lambda inner: inner * 2, lambda inner: inner * 2 + 1,
                  number)


def from_integer(number):
    """The term for a natural number, with no leading zeros."""
    if number == 0:
        return LSB
    bits = []
    remaining = number
    while remaining:
        bits.append(remaining % 2)
        remaining //= 2
    result = LSB
    for bit in bits:
        result = one(result) if bit else zero(result)
    return result


def shift(number):
    """Doubles the value by adding a zero bit at the bottom.

    Written with the fold, as the exam requires: rebuild the number with the
    same bits and put a zero above the marker.
    """
    return fold_b(zero(LSB), zero, one, number)


def rlz(number):
    """Removes the leading zeros without changing the value.

    The leading zeros are the outermost constructors, since the outermost bit
    is the most significant one. Dropping them is therefore a walk from the
    outside in, and it stops at the first one bit or at the marker.
    """
    current = number
    while adt.name_of(current) == "Zero":
        current = adt.arguments_of(current)[0]
    return current


def equals(first, second):
    """The equality instance: different representations of a number are equal."""
    return rlz(first) == rlz(second)


def length(number):
    """How many constructors the term uses."""
    return fold_b(1, lambda inner: inner + 1, lambda inner: inner + 1, number)
