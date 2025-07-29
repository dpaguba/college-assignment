"""Pseudo random generators: deterministic streams that look random.

A linear congruential generator multiplies, adds and takes a remainder, and
its whole quality lies in the three constants. Hull and Dobell say the period
is full exactly when the increment is coprime to the modulus, every prime
factor of the modulus divides the multiplier minus one, and four divides both
or neither. The module checks the condition and the period separately, so the
theorem is verified rather than assumed.

Determinism is the feature, not a defect. A simulation has to be repeatable,
and repeatability means the same seed gives the same stream.
"""


def lcg(seed, multiplier, increment, modulus):
    """A linear congruential generator, as an endless stream of integers."""
    value = seed
    while True:
        value = (multiplier * value + increment) % modulus
        yield value


def period(seed, multiplier, increment, modulus):
    """How many values the generator produces before repeating."""
    stream = lcg(seed, multiplier, increment, modulus)
    seen = {}
    for index in range(modulus + 1):
        value = next(stream)
        if value in seen:
            return index - seen[value]
        seen[value] = index
    return modulus


def has_full_period(multiplier, increment, modulus):
    """The Hull and Dobell condition for a full period."""
    if _gcd(increment, modulus) != 1:
        return False
    for prime in _prime_factors(modulus):
        if (multiplier - 1) % prime:
            return False
    if modulus % 4 == 0 and (multiplier - 1) % 4:
        return False
    return True


def _gcd(first, second):
    """The greatest common divisor."""
    while second:
        first, second = second, first % second
    return first


def _prime_factors(value):
    """The distinct prime factors of a number."""
    factors = set()
    remaining = value
    divisor = 2
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            factors.add(divisor)
            remaining //= divisor
        divisor += 1
    if remaining > 1:
        factors.add(remaining)
    return factors


def uniform_sample(count, seed=0, modulus=2 ** 31, multiplier=1103515245,
                   increment=12345):
    """A sample of values in the unit interval from a generator."""
    stream = lcg(seed, multiplier, increment, modulus)
    return [next(stream) / modulus for _ in range(count)]


def is_reproducible():
    """Whether the same seed gives the same stream, which a simulation needs."""
    first = uniform_sample(20, seed=5)
    second = uniform_sample(20, seed=5)
    return first == second
