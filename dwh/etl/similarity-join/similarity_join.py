"""Matching records that do not match exactly, without comparing all pairs.

A similarity join pairs records whose distance is below a threshold, and the
naive version compares every pair, which is quadratic. Blocking compares only
records sharing a key such as the first letter or a Soundex code, which is
linear in the blocks and can miss a pair whose key differs.

That miss is the trade and it is not hypothetical: two spellings of a name
that differ in the first letter land in different blocks and are never
compared, however similar they are.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "transformation"))
import transformation


def by_edit_distance(left, right, maximum):
    """Every pair within the given edit distance."""
    return [(first, second) for first in left for second in right
            if transformation.edit_distance(first, second) <= maximum]


def jaccard(first, second):
    """The Jaccard similarity of the token sets of two strings."""
    left, right = set(first.split()), set(second.split())
    union = left | right
    return len(left & right) / len(union) if union else 1.0


def blocking_effect(size):
    """How many comparisons blocking saves on a synthetic data set."""
    names = ["name%d" % index for index in range(size)]
    without = len(names) ** 2
    blocks = {}
    for name in names:
        blocks.setdefault(name[:5], []).append(name)
    with_blocking = sum(len(block) ** 2 for block in blocks.values())
    return {"without blocking": without, "with blocking": with_blocking,
            "blocks": len(blocks)}


def blocking_misses():
    """Whether blocking on the first letter can miss a similar pair.

    Two spellings differing in the first letter are close under the edit
    distance and land in different blocks, so they are never compared. The
    usual repair is to block on something less fragile, such as a phonetic
    code, which moves the problem rather than removing it.
    """
    left, right = "Meier", "Neier"
    close = transformation.edit_distance(left, right) <= 1
    same_block = left[0] == right[0]
    return close and not same_block
