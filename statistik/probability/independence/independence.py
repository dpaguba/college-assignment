"""Independence, and the two ways it is stronger than it looks.

Two events are independent when their probabilities multiply, which is a
statement about numbers rather than about causation. Three events can be
independent in every pair and still not be independent together, and that is
the standard warning of the chapter.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "probability-spaces"))
import probability_spaces


def are_independent(space, first, second, tolerance=1e-9):
    """Whether the probability of both equals the product."""
    joint = space.probability(set(first) & set(second))
    return abs(joint - space.probability(first) * space.probability(second)) \
        < tolerance


def pairwise_not_jointly():
    """The classic example: two fair coins and their agreement.

    The three events "first is heads", "second is heads" and "they agree" are
    independent in every pair, and knowing any two determines the third, so
    they are not independent together.
    """
    space = probability_spaces.uniform(["HH", "HT", "TH", "TT"])
    first = {"HH", "HT"}
    second = {"HH", "TH"}
    agree = {"HH", "TT"}
    pairwise = all(are_independent(space, left, right)
                   for left, right in ((first, second), (first, agree),
                                       (second, agree)))
    triple = space.probability(first & second & agree)
    product = (space.probability(first) * space.probability(second)
               * space.probability(agree))
    return {"pairwise": pairwise, "jointly": abs(triple - product) < 1e-9}


def product_inequality():
    """Whether the joint probability is above or below the product.

    The fourth sheet asks whether either inequality holds in general. Neither
    does, and both directions occur, which this function demonstrates with
    two events in one space.
    """
    space = probability_spaces.uniform(range(4))
    same = {0, 1}
    overlapping = {0, 1}
    disjoint = {2, 3}
    greater = space.probability(same & overlapping) > \
        space.probability(same) * space.probability(overlapping)
    smaller = space.probability(same & disjoint) < \
        space.probability(same) * space.probability(disjoint)
    return {"greater exists": greater, "smaller exists": smaller}


def conditional_independence_differs():
    """Whether independence can be created or destroyed by conditioning.

    Two independent events can become dependent once a third is known, which
    is why "independent" is always relative to the information assumed.
    """
    space = probability_spaces.uniform(["HH", "HT", "TH", "TT"])
    first = {"HH", "HT"}
    second = {"HH", "TH"}
    agree = {"HH", "TT"}
    before = are_independent(space, first, second)
    restricted = probability_spaces.uniform(sorted(agree))
    after = are_independent(restricted, first & agree, second & agree)
    return before and not after
