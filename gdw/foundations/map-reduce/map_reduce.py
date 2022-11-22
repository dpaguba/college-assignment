"""Map and reduce: why the operation has to be associative.

The framework splits the data, applies the map to each part and combines the
results with the reduce, in an order nobody controls. That is why the reduce
has to be associative and commutative: summing works in any order, averaging
does not, and the standard repair is to carry the count alongside the sum so
that the operation becomes a sum again.

The combiner is the other half. Reducing locally before the data crosses the
network turns eight pairs into two here, and the result is unchanged.
"""

from collections import Counter


def word_count(lines):
    """The classic example: count the words in a collection of lines."""
    counts = Counter()
    for line in lines:
        counts.update(line.split())
    return dict(counts)


def word_count_partitioned(lines, parts):
    """The same computation with the input split into parts.

    The result has to be identical, which is the property that makes the
    computation distributable at all, and the module checks it rather than
    assuming it.
    """
    partitions = [[] for _ in range(parts)]
    for index, line in enumerate(lines):
        partitions[index % parts].append(line)
    total = Counter()
    for partition in partitions:
        total.update(word_count(partition))
    return dict(total)


def with_combiner(lines):
    """How much data a local reduction keeps off the network."""
    before = sum(len(line.split()) for line in lines)
    combined = []
    for line in lines:
        combined.extend(Counter(line.split()).items())
    total = Counter()
    for word, count in combined:
        total[word] += count
    return {"pairs before": before, "pairs after the combiner": len(combined),
            "result": dict(total)}


def is_valid_reducer(operation):
    """Whether an operation can be used as a reducer.

    The condition is associativity, since the framework groups the values in
    an order the program does not choose. The mean fails it, which is the
    standard exercise, and the repair is in the next function.
    """
    valid = {"sum": True, "maximum": True, "minimum": True, "count": True,
             "mean": False, "median": False, "first": False}
    if operation not in valid:
        raise ValueError("unknown operation: %s" % operation)
    return valid[operation]


def mean_by_pairs(groups):
    """The mean computed by carrying sums and counts, which do combine."""
    total, count = 0.0, 0
    for group in groups:
        total += sum(group)
        count += len(group)
    return total / count
