"""The model: map, shuffle, reduce, and the key that decides the parallelism.

The map runs on each input independently, the shuffle groups by key, and the
reduce runs on each group. The number of reducers does not change the result,
which the module checks, and it does change how the work is spread.

The key decides everything. A key that appears in nearly every record sends
nearly every record to one reducer, and that reducer becomes the run time
whatever the cluster size.
"""

from collections import defaultdict


def word_mapper(line):
    """One pair per word."""
    return [(word, 1) for word in line.split()]


def sum_reducer(key, values):
    """The sum of the values for a key."""
    return sum(values)


def shuffle(pairs):
    """The pairs grouped by key."""
    grouped = defaultdict(list)
    for key, value in pairs:
        grouped[key].append(value)
    return dict(grouped)


def run(records, mapper, reducer, reducers=1):
    """The whole computation, over the given number of reducers."""
    pairs = []
    for record in records:
        pairs.extend(mapper(record))
    grouped = shuffle(pairs)
    partitions = [dict() for _ in range(reducers)]
    for key, values in grouped.items():
        partitions[hash(key) % reducers][key] = values
    result = {}
    for partition in partitions:
        for key, values in partition.items():
            result[key] = reducer(key, values)
    return result


def skew(records, reducers):
    """How unevenly the keys spread over the reducers."""
    counts = [0] * reducers
    for record in records:
        counts[hash(record) % reducers] += 1
    total = sum(counts)
    return {"counts": counts,
            "largest share": max(counts) / total if total else 0.0}
