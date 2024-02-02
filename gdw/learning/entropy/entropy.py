"""Shannon entropy, and the split it justifies.

The eighth sheet derives the entropy from three requirements and then asks
for a concrete distribution: a fair die and a fair coin, with X the sum. X
takes the values 1 and 7 with probability one twelfth each, since only one
outcome gives them, and the values in between with probability one sixth.

Its entropy is 2.7516 bits, against the 2.585 of the die alone: adding the
coin adds information, and adding it to the extremes of the range adds less
than a full bit because those outcomes became rarer.
"""

import math


def shannon(distribution, base=2):
    """The entropy of a distribution, in bits by default."""
    total = 0.0
    for probability in distribution.values():
        if probability > 0:
            total -= probability * math.log(probability, base)
    return total


def die_plus_coin():
    """The distribution of the sum of a fair die and a fair coin."""
    distribution = {}
    for die in range(1, 7):
        for coin in (0, 1):
            value = die + coin
            distribution[value] = distribution.get(value, 0.0) + 1 / 12
    return distribution


def die_minus_coin():
    """The distribution of the difference, which is the mirror image."""
    distribution = {}
    for die in range(1, 7):
        for coin in (0, 1):
            value = die - coin
            distribution[value] = distribution.get(value, 0.0) + 1 / 12
    return distribution


def joint_entropy(pairs):
    """The entropy of a joint distribution over pairs."""
    return shannon(pairs)


def conditional_entropy(pairs):
    """The entropy of the second component given the first."""
    marginal = {}
    for (first, _second), probability in pairs.items():
        marginal[first] = marginal.get(first, 0.0) + probability
    total = 0.0
    for (first, _second), probability in pairs.items():
        if probability > 0:
            total -= probability * math.log(probability / marginal[first], 2)
    return total


def information_gain(labels, parts):
    """How much entropy a split removes."""
    def distribution(values):
        """The empirical distribution of a list of labels."""
        counts = {}
        for value in values:
            counts[value] = counts.get(value, 0) + 1
        return {value: count / len(values) for value, count in counts.items()}

    before = shannon(distribution(labels))
    after = sum(len(part) / len(labels) * shannon(distribution(part))
                for part in parts if part)
    return before - after
