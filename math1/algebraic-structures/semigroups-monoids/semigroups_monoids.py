"""One operation, and the three conditions that can be added to it.

A magma is a set with an operation. Requiring associativity gives a
semigroup, an identity gives a monoid, and inverses give a group. The counts
show how much each condition costs: of the 16 operations on a two-element
set, 8 are associative, and of the 19683 on a three-element set, 113 are.
"""

import itertools


def is_closed(base, operation):
    """Whether the operation stays inside the set."""
    items = list(base)
    return all(operation(left, right) in items
               for left in items for right in items)


def modular_table(modulus, kind):
    """The table of an operation on the numbers below the modulus."""
    if kind == "add":
        return {(left, right): (left + right) % modulus
                for left in range(modulus) for right in range(modulus)}
    if kind == "multiply":
        return {(left, right): (left * right) % modulus
                for left in range(modulus) for right in range(modulus)}
    if kind == "subtract":
        return {(left, right): (left - right) % modulus
                for left in range(modulus) for right in range(modulus)}
    raise ValueError("unknown operation: %s" % kind)


def carrier(table):
    """The elements the table is defined on."""
    return sorted({item for pair in table for item in pair})


def is_associative(table):
    """Whether the bracketing never matters."""
    items = carrier(table)
    for left in items:
        for middle in items:
            for right in items:
                if table[(table[(left, middle)], right)] != \
                        table[(left, table[(middle, right)])]:
                    return False
    return True


def identities(table):
    """Every element that leaves the others unchanged on both sides."""
    items = carrier(table)
    return [candidate for candidate in items
            if all(table[(candidate, other)] == other
                   and table[(other, candidate)] == other for other in items)]


def identity(table):
    """The identity, or nothing when the structure has none.

    Uniqueness is worth stating as a computation: if two identities existed,
    each would have to leave the other unchanged, so they would be equal, and
    the list this function reads from never has two entries.
    """
    found = identities(table)
    return found[0] if found else None


def count_associative(size):
    """How many operations on a set of the given size are associative."""
    items = list(range(size))
    pairs = [(left, right) for left in items for right in items]
    total = 0
    for values in itertools.product(items, repeat=len(pairs)):
        table = dict(zip(pairs, values))
        if is_associative(table):
            total += 1
    return total


def free_monoid(alphabet, length):
    """Every word over the alphabet up to the given length, with the empty one."""
    words = [""]
    for size in range(1, length + 1):
        for letters in itertools.product(alphabet, repeat=size):
            words.append("".join(letters))
    return words


def generated(table, generators):
    """The smallest subset containing the generators and closed under the table."""
    found = set(generators)
    identity_element = identity(table)
    if identity_element is not None:
        found.add(identity_element)
    while True:
        additions = {table[(left, right)] for left in found for right in found
                     if table[(left, right)] not in found}
        if not additions:
            return found
        found |= additions
