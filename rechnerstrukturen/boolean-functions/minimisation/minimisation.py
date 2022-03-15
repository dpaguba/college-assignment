"""Quine and McCluskey: from a truth vector to a minimal cover.

Two steps, and they are different problems. Finding the **prime implicants** is
mechanical: repeatedly combine two terms that differ in one position, replacing
that position by a dash, until nothing combines. Choosing a **minimal subset**
that covers every one-row is set cover, which is NP-hard, so the algorithm is
exact and exponential.

The first step is what the exercise sheets ask to tabulate, level by level,
because the levels are where the work is visible.
"""

from __future__ import annotations

import itertools


def levels(vector):
    """Each round of combining, starting from the minterms.

    Level `i` holds the terms with `i` dashes. A term that combines with
    another is marked as covered; what remains uncovered at every level is a
    prime implicant, since nothing absorbed it.
    """
    variables = (len(vector) - 1).bit_length()
    current = [format(index, f"0{variables}b")
               for index, value in enumerate(vector) if value]
    result = [sorted(current)]

    while current:
        combined = set()
        used = set()

        for first, second in itertools.combinations(current, 2):
            position = _single_difference(first, second)
            if position is None:
                continue
            used.add(first)
            used.add(second)
            combined.add(first[:position] + "-" + first[position + 1:])

        if not combined:
            break

        result.append(sorted(combined))
        current = sorted(combined)

    return result


def _single_difference(first, second):
    """The position where two terms differ, if there is exactly one."""
    positions = [index for index, (a, b) in enumerate(zip(first, second)) if a != b]
    if len(positions) != 1:
        return None
    if any(first[index] == "-" or second[index] == "-" for index in positions):
        return None
    return positions[0]


def prime_implicants(vector):
    """Every term that no further combination absorbs."""
    variables = (len(vector) - 1).bit_length()
    current = [format(index, f"0{variables}b")
               for index, value in enumerate(vector) if value]
    primes = set()

    while current:
        combined = set()
        used = set()

        for first, second in itertools.combinations(current, 2):
            position = _single_difference(first, second)
            if position is None:
                continue
            used.add(first)
            used.add(second)
            combined.add(first[:position] + "-" + first[position + 1:])

        primes |= {term for term in current if term not in used}
        current = sorted(combined)

    return sorted(primes)


def covers(term, index, variables):
    """Whether an implicant covers a row."""
    pattern = format(index, f"0{variables}b")
    return all(position == "-" or position == bit
               for position, bit in zip(term, pattern))


def essential_primes(vector):
    """Primes that are the only cover of some one-row.

    Every minimal cover contains all of them, which is what makes the
    exhaustive search over the rest tractable: the essential primes are free
    and only the remainder needs deciding.
    """
    variables = (len(vector) - 1).bit_length()
    primes = prime_implicants(vector)
    ones = [index for index, value in enumerate(vector) if value]
    essential = set()

    for index in ones:
        covering = [term for term in primes if covers(term, index, variables)]
        if len(covering) == 1:
            essential.add(covering[0])

    return sorted(essential)


def minimal_cover(vector):
    """The smallest set of primes covering every one-row.

    Set cover, solved exactly by taking the essential primes and searching over
    subsets of the rest. Exponential, and small enough for the five variables
    an exercise uses.
    """
    variables = (len(vector) - 1).bit_length()
    primes = prime_implicants(vector)
    ones = [index for index, value in enumerate(vector) if value]

    if not ones:
        return []

    essential = essential_primes(vector)
    remaining = [index for index in ones
                 if not any(covers(term, index, variables) for term in essential)]

    if not remaining:
        return essential

    others = [term for term in primes if term not in essential]

    for size in range(1, len(others) + 1):
        for candidate in itertools.combinations(others, size):
            if all(any(covers(term, index, variables) for term in candidate)
                   for index in remaining):
                return sorted(essential + list(candidate))

    return primes


def implicant_text(term, variables):
    """One implicant as a conjunction, dashes omitted."""
    parts = []
    for name, value in zip(variables, term):
        if value == "1":
            parts.append(name)
        elif value == "0":
            parts.append(f"!{name}")
    return " ".join(parts) if parts else "1"


def evaluate(cover, index, variables):
    """Whether a cover accepts a row."""
    return any(covers(term, index, variables) for term in cover)


def literal_count(cover, variables):
    """How many literals the cover uses, which is the usual cost measure.

    Terms alone are not the cost: a two-term cover of five literals each is
    larger than a three-term cover of two. Counting literals is what a gate
    count actually follows.
    """
    return sum(sum(1 for position in term if position != "-") for term in cover)
