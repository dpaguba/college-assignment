"""Lazy evaluation: a value computed only if it is needed.

Haskell evaluates to weak head normal form on demand, so a definition may
mention an infinite list and a computation that never terminates, as long as
nothing forces them. The exam asks for an infinite list of solutions that is
productive, which is exactly this property: `take 2` has to finish even
though the list does not.

Generators stand in for laziness here. What they reproduce is the part that
matters: producing one element at a time and never computing an element that
is not taken.
"""

import itertools


def take(count, stream):
    """The first values of a stream."""
    return list(itertools.islice(stream, count))


def naturals():
    """The natural numbers, one at a time."""
    value = 0
    while True:
        yield value
        value += 1


def fibonacci():
    """The Fibonacci numbers as a stream."""
    first, second = 0, 1
    while True:
        yield first
        first, second = second, first + second


def primes():
    """The primes, by a sieve that keeps the divisors found so far."""
    found = []
    for candidate in itertools.count(2):
        if all(candidate % prime for prime in found
               if prime * prime <= candidate):
            found.append(candidate)
            yield candidate


def solutions():
    """The exam's infinite list of triples with 5x + y² + 10 = z.

    Productive means every prefix is reachable in finite time, so the search
    cannot be a loop over x with an inner loop over y: that would never leave
    x = 0. Enumerating the pairs diagonally reaches every pair eventually,
    which is the same argument as the countability of the pairs of naturals.
    """
    for total in itertools.count(0):
        for x in range(total + 1):
            y = total - x
            yield (x, y, 5 * x + y * y + 10)


def diverge():
    """A computation that never finishes, used to show what is not forced."""
    while True:
        pass


def lazy_and(thunks):
    """The conjunction, stopping at the first false value.

    The second argument is never forced when the first is false, which is why
    a diverging thunk can sit in the list without the computation diverging.
    """
    for thunk in thunks:
        if not thunk():
            return False
    return True


def count_evaluations():
    """How many of three defined values a lazy consumer actually computes."""
    computed = []

    def make(value):
        """A thunk that records when it is forced."""
        def thunk():
            """Forces the value and records the fact."""
            computed.append(value)
            return value
        return thunk

    thunks = [make(1), make(2), make(3)]
    thunks[0]()
    return {"defined": len(thunks), "computed": len(computed)}
