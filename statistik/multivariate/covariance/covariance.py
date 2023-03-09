"""Covariance and correlation of two random variables.

Covariance is the expectation of the product of the deviations. It is zero
for independent variables, and the converse fails: a symmetric dependence
gives zero covariance with complete dependence, which is the warning of the
chapter and the reason correlation is a measure of linear association only.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "joint-distributions"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "random-variables", "expectation-variance"))
import expectation_variance
import joint_distributions


def covariance(joint):
    """The expected product of the two deviations."""
    first, second = joint_distributions.margins(joint)
    mean_first = expectation_variance.expectation(first)
    mean_second = expectation_variance.expectation(second)
    return sum((left - mean_first) * (right - mean_second) * weight
               for (left, right), weight in joint.items())


def correlation(joint):
    """The covariance divided by the two standard deviations."""
    first, second = joint_distributions.margins(joint)
    spread = (expectation_variance.standard_deviation(first)
              * expectation_variance.standard_deviation(second))
    if spread == 0:
        raise ValueError("a constant variable has no correlation")
    return covariance(joint) / spread


def uncorrelated_but_dependent():
    """A joint distribution with zero covariance and complete dependence.

    The second variable is the square of the first, and the first is
    symmetric about zero. Knowing one determines the other, and the
    covariance is exactly zero.
    """
    return {(-1, 1): 1 / 3, (0, 0): 1 / 3, (1, 1): 1 / 3}
