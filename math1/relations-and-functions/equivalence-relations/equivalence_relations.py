"""Equivalence relations and partitions, which are the same thing twice.

Every equivalence relation cuts its set into classes, and every partition
defines a relation whose classes are the parts. The two constructions are
inverse to each other, so a statement about one is a statement about the
other, and the number of either on a set of n elements is the Bell number.
"""


def from_partition(partition):
    """The relation whose classes are the parts."""
    relation = set()
    for part in partition:
        for left in part:
            for right in part:
                relation.add((left, right))
    return relation


def to_partition(relation, base):
    """The classes of an equivalence relation."""
    classes = []
    placed = set()
    for element in base:
        if element in placed:
            continue
        part = {other for other in base if (element, other) in relation}
        classes.append(part)
        placed |= part
    return classes


def partitions(base):
    """Every partition of the set, as a list of lists of sets."""
    if not base:
        return [[]]
    first, rest = base[0], base[1:]
    result = []
    for partition in partitions(rest):
        for index in range(len(partition)):
            copy = [set(part) for part in partition]
            copy[index].add(first)
            result.append(copy)
        result.append([set(part) for part in partition] + [{first}])
    return result


def bell_number(size):
    """How many partitions a set of the given size has."""
    row = [1]
    for _ in range(size):
        following = [row[-1]]
        for value in row:
            following.append(following[-1] + value)
        row = following
    return row[0]


def congruence(modulus, divisor):
    """Congruence modulo the divisor, on the numbers below the modulus."""
    return {(left, right) for left in range(modulus) for right in range(modulus)
            if (left - right) % divisor == 0}


def class_of(element, relation, base):
    """The class an element belongs to."""
    return {other for other in base if (element, other) in relation}
