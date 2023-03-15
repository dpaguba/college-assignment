"""Probability spaces: outcomes, events, and the three axioms.

An event is a set of outcomes, so the operations on events are the set
operations, and every rule of the chapter follows from three axioms:
probabilities are non-negative, the whole space has probability one, and
disjoint events add. The addition rule for overlapping events, the
complement rule and monotonicity are all consequences, and the module derives
them rather than restating them.
"""


class Space:
    """A finite probability space, given by the probability of each outcome."""

    def __init__(self, weights):
        """A space over the keys of the mapping, with those probabilities."""
        self.weights = dict(weights)

    def outcomes(self):
        """Every outcome the space knows."""
        return set(self.weights)

    def probability(self, event):
        """The probability of an event, which is a set of outcomes."""
        unknown = set(event) - self.outcomes()
        if unknown:
            raise ValueError("outcomes outside the space: %s" % sorted(unknown,
                                                                       key=str))
        return sum(self.weights[outcome] for outcome in event)


def uniform(outcomes):
    """The space in which every outcome is equally likely."""
    outcomes = list(outcomes)
    return Space({outcome: 1 / len(outcomes) for outcome in outcomes})


def is_measure(space, tolerance=1e-9):
    """Whether the weights satisfy the axioms."""
    if any(value < 0 for value in space.weights.values()):
        return False
    return abs(sum(space.weights.values()) - 1) < tolerance


def complement(space, event):
    """The probability of an event not happening."""
    return 1 - space.probability(event)


def union(space, first, second):
    """The addition rule, which subtracts the overlap counted twice."""
    return (space.probability(first) + space.probability(second)
            - space.probability(set(first) & set(second)))
