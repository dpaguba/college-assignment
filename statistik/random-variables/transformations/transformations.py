"""Transformations of a random variable, and what they do to its moments.

A linear transformation moves the expectation the same way and scales the
variance by the square, which is why the standard deviation and not the
variance is measured in the units of the variable. A transformation that is
not injective merges probabilities, and the merged distribution is generally
not a linear image of the original.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "expectation-variance"))
import expectation_variance


def apply(weights, mapping):
    """The distribution of the transformed variable."""
    result = {}
    for value, weight in weights.items():
        image = mapping(value)
        result[image] = result.get(image, 0.0) + weight
    return result


def linear(weights, factor, offset):
    """The distribution after multiplying and shifting."""
    return apply(weights, lambda value: factor * value + offset)


def standardise(weights):
    """The distribution shifted and scaled to mean zero and variance one."""
    centre = expectation_variance.expectation(weights)
    spread = expectation_variance.standard_deviation(weights)
    if spread == 0:
        raise ValueError("a constant variable cannot be standardised")
    return linear(weights, 1 / spread, -centre / spread)


def indicator(weights, event):
    """The distribution of the indicator of an event.

    Its expectation is the probability of the event, which is the bridge
    between the language of events and the language of random variables.
    """
    return apply(weights, lambda value: 1 if value in event else 0)
