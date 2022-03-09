"""Counting the infinite: pairing, enumeration, and the diagonal argument.

Two questions look alike and have opposite answers. The pairs of naturals can
be listed, and so can the rationals, because a listing only has to reach every
element eventually. The infinite binary sequences cannot, and the reason is
the diagonal: given any listing, one can write down an element that differs
from the first in the first place, from the second in the second, and so on.
"""

from fractions import Fraction


def pair(first, second):
    """The Cantor pairing of two naturals, a bijection onto the naturals."""
    total = first + second
    return total * (total + 1) // 2 + second


def unpair(code):
    """The two naturals a code came from."""
    total = 0
    while (total + 1) * (total + 2) // 2 <= code:
        total += 1
    second = code - total * (total + 1) // 2
    return total - second, second


def enumerate_rationals(count):
    """The first rationals in an enumeration that repeats nothing."""
    listed = []
    seen = set()
    code = 0
    while len(listed) < count:
        numerator, denominator = unpair(code)
        code += 1
        if denominator == 0:
            continue
        for sign in (1, -1):
            value = Fraction(sign * numerator, denominator)
            if value not in seen:
                seen.add(value)
                listed.append(value)
                if len(listed) == count:
                    break
    return listed


def diagonal(listing):
    """A sequence differing from every listed sequence in one position.

    The construction is the whole argument. It needs no assumption about how
    the listing was produced, so no listing can be complete, and the set is
    therefore not countable.
    """
    return [(row[index] + 1) % 10 for index, row in enumerate(listing)]


def sample_maps(base, count):
    """A sample of maps from the set into its power set."""
    items = sorted(base)
    maps = []
    for seed in range(count):
        mapping = {}
        for position, item in enumerate(items):
            value = (seed >> (position * 2)) % (2 ** len(items))
            mapping[item] = frozenset(other for index, other in enumerate(items)
                                      if value >> index & 1)
        maps.append(mapping)
    return maps


def cantor_witness(base, mapping):
    """The subset no element is mapped to, which exists for every map.

    Built by taking each element that its own image leaves out. That subset
    differs from every image in at least one element, so the map misses it,
    which is Cantor's theorem for the finite case and the same argument as
    the diagonal for the infinite one.
    """
    witness = frozenset(item for item in base if item not in mapping[item])
    for item in base:
        if mapping[item] == witness:
            return None
    return witness
