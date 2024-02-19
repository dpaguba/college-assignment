"""MinHash: estimating a similarity without comparing the sets.

Take a random permutation of the universe and record the smallest element of
each set under it. The two minima agree exactly when the smallest element of
the union lies in the intersection, which happens with probability equal to
the Jaccard similarity. Repeating with many permutations turns that
probability into an estimate.

The point is the size. A set of ten thousand elements becomes a signature of
a hundred numbers, comparisons cost a hundred integer equalities instead of
a set intersection, and the error falls with the square root of the signature
length.
"""

import random


MASK = (1 << 64) - 1
"""The word size the mixer works in."""


def _mix(value):
    """A strong 64 bit mixer, the finaliser of the splitmix64 generator.

    Python's own hash of a small tuple is structured enough to bias the
    minimum: with it, the estimate of a similarity of 0.667 came out at 0.69
    and one of 0.333 at 0.306, consistently, over many permutations. A proper
    avalanche removes that.
    """
    value &= MASK
    value ^= value >> 30
    value = (value * 0xBF58476D1CE4E5B9) & MASK
    value ^= value >> 27
    value = (value * 0x94D049BB133111EB) & MASK
    return value ^ (value >> 31)


def _salts(hashes, seed):
    """One salt per permutation, which stands for the permutation itself."""
    generator = random.Random(seed)
    return [generator.randrange(1 << 62) for _ in range(hashes)]


def signature(values, hashes, seed=0):
    """The smallest hash of the set under each permutation."""
    salts = _salts(hashes, seed)
    if not values:
        return [0] * hashes
    mixed = [_mix(hash(value)) for value in values]
    return [min(_mix(item ^ salt) for item in mixed) for salt in salts]


def estimate(first, second, hashes, seed=0):
    """The share of the signature positions that agree."""
    left = signature(first, hashes, seed)
    right = signature(second, hashes, seed)
    matches = sum(1 for a, b in zip(left, right) if a == b)
    return matches / len(left)


def expected_error(hashes, similarity_value):
    """The standard error of the estimate, which falls with the root."""
    return (similarity_value * (1 - similarity_value) / hashes) ** 0.5
