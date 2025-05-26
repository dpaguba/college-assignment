"""Samplesort: quicksort with many pivots at once, the sort of clusters.

Several candidates are sampled per pivot before choosing. More oversampling
means more even buckets and more sampling cost.
"""

from __future__ import annotations

import random
from bisect import bisect_right

SMALL = 32
OVERSAMPLING = 3

def samplesort(items, key=None, buckets=8, seed=None):
    """Return a sorted copy of `items`.

    Quicksort splits into two parts, which is exactly wrong when there are
    sixteen processors waiting. Samplesort takes a random sample, sorts it,
    picks k-1 pivots out of it, and splits the input into k buckets at once.
    Every bucket is independent, so each machine or thread takes one and sorts
    it alone, and concatenating the results needs no merge step at all.

    That is why it is the standard sort for distributed systems and GPUs. The
    sample is what makes the buckets roughly equal; with a bad sample one
    bucket swallows everything and the parallelism evaporates.
    """
    values = list(items)
    of = key or (lambda item: item)
    generator = random.Random(seed)

    def sort(subset):
        """Sorts the subset by splitting it at sampled pivots."""
        if len(subset) <= SMALL:
            return sorted(subset, key=of)

        count = min(buckets, len(subset))
        sample_size = min(len(subset), OVERSAMPLING * count)
        sample = sorted(
            (of(value) for value in generator.sample(subset, sample_size)),
        )
        step = len(sample) / count
        pivots = [sample[int(index * step)] for index in range(1, count)]
        pivots = sorted(set(pivots))
        if not pivots:
            return sorted(subset, key=of)

        parts: list[list] = [[] for _ in range(len(pivots) + 1)]
        for value in subset:
            parts[bisect_right(pivots, of(value))].append(value)

        if max(len(part) for part in parts) == len(subset):
            return sorted(subset, key=of)

        return [value for part in parts for value in sort(part)]

    return sort(values)
