"""Sums of random variables, and the condition variances need.

Expectations always add. Variances add only when the variables are
uncorrelated, and in general the covariance appears twice:

    Var(X + Y) = Var(X) + Var(Y) + 2 Cov(X, Y).

The convolution below computes the distribution of a sum of two independent
variables, which is where the binomial's additivity comes from: two binomials
with the same success chance add to a binomial.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "joint-distributions"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "covariance"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "random-variables", "expectation-variance"))
import covariance
import expectation_variance
import joint_distributions


def convolve(first, second):
    """The distribution of the sum of two independent variables."""
    result = {}
    for left, left_weight in first.items():
        for right, right_weight in second.items():
            total = left + right
            result[total] = result.get(total, 0.0) + left_weight * right_weight
    return result


def sum_distribution(joint):
    """The distribution of the sum, for a possibly dependent pair."""
    result = {}
    for (left, right), weight in joint.items():
        total = left + right
        result[total] = result.get(total, 0.0) + weight
    return result


def dependent_sum():
    """A dependent pair whose variances do not add.

    The two variables are perfectly negatively related, so the sum is
    constant and its variance is zero while each part has a positive
    variance. The covariance term is what closes the gap.
    """
    joint = {(0, 1): 0.5, (1, 0): 0.5}
    first, second = joint_distributions.margins(joint)
    return {"variance of the sum":
            expectation_variance.variance(sum_distribution(joint)),
            "sum of the variances": (expectation_variance.variance(first)
                                     + expectation_variance.variance(second)),
            "covariance": covariance.covariance(joint)}
