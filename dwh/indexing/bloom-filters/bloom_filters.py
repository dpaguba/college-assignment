"""A Bloom filter: membership with false positives and no false negatives.

Several hash functions set bits; a lookup checks them all. A member always
passes, because its bits were set, and a non-member passes only if every one
of its bits happened to be set by others, which is the false positive rate.

The lecture uses it to accelerate a star join: send a small filter of the
qualifying dimension keys to the fact table scan and discard most of the rows
before any join happens. The filter is small enough to fit anywhere, which is
the whole point.
"""

import math


def build(items, bits, hashes):
    """The bit array with every item inserted."""
    array = [0] * bits
    for item in items:
        for index in _positions(item, bits, hashes):
            array[index] = 1
    return {"bits": array, "hashes": hashes, "size": bits}


def _positions(item, bits, hashes):
    """The bit positions an item touches."""
    return [(_mix(hash(item) ^ (salt * 0x9E3779B97F4A7C15)) % bits)
            for salt in range(hashes)]


def _mix(value):
    """A 64 bit avalanche mixer."""
    mask = (1 << 64) - 1
    value &= mask
    value ^= value >> 30
    value = (value * 0xBF58476D1CE4E5B9) & mask
    value ^= value >> 27
    value = (value * 0x94D049BB133111EB) & mask
    return value ^ (value >> 31)


def contains(filter_, item):
    """Whether the item might be present."""
    return all(filter_["bits"][index]
               for index in _positions(item, filter_["size"],
                                       filter_["hashes"]))


def false_positive_rate(bits, items, hashes):
    """The predicted rate for the given parameters."""
    return (1 - math.exp(-hashes * items / bits)) ** hashes


def optimal_hashes(bits, items):
    """The number of hash functions minimising the error rate."""
    return max(1, round(bits / items * math.log(2)))


def no_false_negatives():
    """Whether a member can ever be reported as absent.

    It cannot, by construction: its bits were set when it was inserted and
    nothing clears them. That asymmetry is what makes the filter usable as a
    pre-filter, since a discarded row is certainly not a match.
    """
    filter_ = build([str(index) for index in range(200)], bits=2048, hashes=4)
    return all(contains(filter_, str(index)) for index in range(200))
