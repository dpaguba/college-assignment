"""Defining a set by rules, and what "the smallest such set" means.

An inductive definition names some elements outright and gives rules that
produce new elements from old ones. The set defined is the smallest one
closed under the rules, and that phrase is a computation: apply the rules
until nothing new appears. Every recursive definition in the course is an
instance, including the terms of a signature and the Fibonacci numbers.
"""

from math import isqrt


def generate(rules, limit=1000):
    """The least set closed under the rules.

    Each rule is a pair of a premise set and a conclusion, so a rule fires
    once all of its premises are present. Iterating to a fixed point is the
    definition rather than an implementation of it.
    """
    generated = set()
    for _ in range(limit):
        additions = {conclusion for premises, conclusion in rules
                     if set(premises) <= generated and conclusion not in generated}
        if not additions:
            return generated
        generated |= additions
    raise ValueError("the generation did not settle within the limit")


def terms(depth, constants, operations):
    """Every term of the signature built with at most the given nesting.

    The count grows quickly: two constants and one binary operation give
    2, 6 and 38 terms at depths 0, 1 and 2. The recurrence is
    t(n+1) = c + t(n)^2 with c the number of constants, since a term of the
    next depth is either a constant or the operation applied to two terms of
    the current one, and the terms already built are not counted twice.
    """
    built = set(constants)
    for _ in range(depth):
        additions = set()
        for name, arity in operations:
            for arguments in _tuples(sorted(built), arity):
                additions.add("%s(%s)" % (name, ",".join(arguments)))
        built |= additions
    return built


def _tuples(items, length):
    """Every tuple of the given length over the items."""
    if length == 0:
        return [()]
    smaller = _tuples(items, length - 1)
    return [(item,) + rest for item in items for rest in smaller]


def fibonacci(index):
    """The Fibonacci number, by the recursion the lecture gives."""
    first, second = 0, 1
    for _ in range(index):
        first, second = second, first + second
    return first


def fibonacci_closed(index):
    """The same number from the closed form, as an integer.

    Binet's formula in floating point loses the value quickly, so the closed
    form is evaluated in exact integer arithmetic over the ring Z[phi],
    represented as pairs. The two definitions then agree exactly rather than
    approximately.
    """
    def multiply(left, right):
        """The product in the ring, where phi squared is phi plus one."""
        first = left[0] * right[0] + left[1] * right[1]
        second = left[0] * right[1] + left[1] * right[0] + left[1] * right[1]
        return (first, second)

    result, power, exponent = (1, 0), (0, 1), index
    while exponent:
        if exponent & 1:
            result = multiply(result, power)
        power = multiply(power, power)
        exponent >>= 1
    return result[1]


def is_well_founded(steps, base):
    """Whether every element reduces to a base element in finitely many steps."""
    reachable = set(base)
    for _ in range(len(steps) + len(base) + 1):
        additions = {source for source, target in steps
                     if target in reachable and source not in reachable}
        if not additions:
            break
        reachable |= additions
    return all(source in reachable for source, _ in steps)


def is_square(value):
    """Whether the value is a perfect square, used by the term exercises."""
    root = isqrt(value)
    return root * root == value
