"""Conditional probability, total probability, and Bayes.

Conditioning restricts the space to the given event and renormalises, so the
formula is a definition rather than a theorem. What follows from it is the
law of total probability, which decomposes an event along a partition, and
Bayes' rule, which reverses the direction of the conditioning.

The seventh sheet is the worked example: from P(pass practice | pass exam) =
0.8, P(pass practice | fail exam) = 0.2 and P(pass exam) = 0.7 it derives
P(pass practice) = 0.62 and P(fail exam | pass practice) = 0.097.
"""


def given(space, event, condition):
    """The probability of an event, given that another one happened."""
    weight = space.probability(condition)
    if weight == 0:
        raise ValueError("cannot condition on an impossible event")
    return space.probability(set(event) & set(condition)) / weight


def total_probability(prior, likelihood):
    """The probability of an event, summed over a partition of the space."""
    return sum(prior[case] * likelihood[case] for case in prior)


def bayes(prior, likelihood):
    """The posterior probability of each case, given that the event happened.

    The reversal is what makes the rule useful and what makes it easy to
    misread: a test that is right 99 percent of the time says little about a
    rare condition, because the prior dominates.
    """
    evidence = total_probability(prior, likelihood)
    if evidence == 0:
        raise ValueError("the evidence has probability zero")
    return {case: prior[case] * likelihood[case] / evidence for case in prior}


def chain(probabilities):
    """The multiplication rule for a sequence of conditional probabilities."""
    result = 1.0
    for value in probabilities:
        result *= value
    return result
