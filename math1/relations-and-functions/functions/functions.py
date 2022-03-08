"""Functions between finite sets, and how many there are of each kind.

The counting is where the definitions become concrete. Maps from a set of
three into a set of four number 64; the injective ones number 24; and
surjections onto a smaller set are counted by inclusion and exclusion, which
is the same principle as in the set chapter applied to a different question.
"""

import itertools
from math import comb, factorial


def is_function(mapping, domain):
    """Whether every element of the domain has exactly one value."""
    return all(element in mapping for element in domain)


def is_injective(mapping):
    """Whether no two arguments share a value."""
    values = list(mapping.values())
    return len(set(values)) == len(values)


def is_surjective(mapping, codomain):
    """Whether every element of the codomain is taken."""
    return set(codomain) <= set(mapping.values())


def is_bijective(mapping, codomain):
    """Both at once, which is what makes an inverse exist."""
    return is_injective(mapping) and is_surjective(mapping, codomain)


def compose(second, first):
    """The map that applies the first and then the second."""
    return {key: second[value] for key, value in first.items()}


def inverse(mapping):
    """The inverse of an injective map."""
    if not is_injective(mapping):
        raise ValueError("only an injective map has an inverse")
    return {value: key for key, value in mapping.items()}


def pigeonhole(mapping):
    """Two arguments with the same value, or nothing when there are none.

    The principle is one line once the map is written down, and the witness
    is what makes it a proof rather than a count.
    """
    seen = {}
    for key, value in sorted(mapping.items(), key=str):
        if value in seen:
            return (seen[value], key)
        seen[value] = key
    return None


def all_functions(domain, codomain):
    """Every map from the domain into the codomain."""
    return [dict(zip(domain, values))
            for values in itertools.product(codomain, repeat=len(domain))]


def count_all(domain_size, codomain_size):
    """How many maps there are between sets of the given sizes."""
    return codomain_size ** domain_size


def count_injective(domain_size, codomain_size):
    """How many of them are injective, which is a falling factorial."""
    if domain_size > codomain_size:
        return 0
    result = 1
    for step in range(domain_size):
        result *= codomain_size - step
    return result


def count_surjective(domain_size, codomain_size):
    """How many are surjective, by inclusion and exclusion over the missed values."""
    total = 0
    for missed in range(codomain_size + 1):
        total += ((-1) ** missed * comb(codomain_size, missed)
                  * (codomain_size - missed) ** domain_size)
    return total


def count_bijective(domain_size, codomain_size):
    """How many are bijective, which needs the sizes to agree."""
    return factorial(domain_size) if domain_size == codomain_size else 0
