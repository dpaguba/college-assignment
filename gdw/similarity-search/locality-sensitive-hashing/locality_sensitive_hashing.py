"""Locality sensitive hashing: finding the neighbours without comparing all pairs.

The signature is split into bands of rows, and two documents become
candidates when they agree on a whole band. The probability of that is a
steep S-curve in the similarity, so the method finds the similar pairs and
skips almost all of the rest.

The threshold is roughly the number of rows raised to the power of minus one
over the bands, which for twenty bands of five rows is 0.55. Below it the
chance of becoming a candidate is small and above it nearly certain, and the
module computes both ends of the curve.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "minhash"))
import minhash


def threshold(bands, rows):
    """The similarity at which a pair becomes likely to be a candidate."""
    return (1 / bands) ** (1 / rows)


def probability(similarity, bands, rows):
    """The chance that a pair of the given similarity becomes a candidate."""
    return 1 - (1 - similarity ** rows) ** bands


def are_candidates(first, second, bands, rows, seed=0):
    """Whether the two sets agree on at least one whole band."""
    left = minhash.signature(first, bands * rows, seed)
    right = minhash.signature(second, bands * rows, seed)
    for band in range(bands):
        start = band * rows
        if left[start:start + rows] == right[start:start + rows]:
            return True
    return False


def pairs_examined(documents, bands, rows, seed=0):
    """How many pairs the method looks at, against all of them.

    The saving is the point: with a hundred documents there are 4950 pairs,
    and the banding leaves only the ones sharing a band, which for a sparse
    collection is a small fraction.
    """
    total = len(documents) * (len(documents) - 1) // 2
    candidates = 0
    for first in range(len(documents)):
        for second in range(first + 1, len(documents)):
            if are_candidates(documents[first], documents[second], bands, rows,
                              seed):
                candidates += 1
    return {"all pairs": total, "candidate pairs": candidates}
