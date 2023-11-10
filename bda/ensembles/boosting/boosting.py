"""AdaBoost: reweighting the data so the next learner sees the mistakes.

Each round fits a classifier to weighted data, computes its weighted error,
gives it a weight of the log odds of being right, and multiplies the weights
of the misclassified points so the next round concentrates on them.

The tenth exercise sheet works through two rounds and the module reproduces
its numbers exactly: an error of 0.3 gives a classifier weight of ln(7/3),
the misclassified points end at one sixth and the rest at one fourteenth, and
the second round gives an error of 0.286 and a weight of 0.916.

A classifier weight is positive when the error is below one half and negative
above it, so a learner that is worse than chance enters the ensemble
inverted, which is why "better than chance" is the only requirement.
"""

import math


def alpha(error):
    """The weight of a classifier with the given weighted error."""
    if error <= 0:
        return float("inf")
    if error >= 1:
        return float("-inf")
    return math.log((1 - error) / error)


def round_one(labels, predictions):
    """The first round, with equal starting weights."""
    weights = [1 / len(labels)] * len(labels)
    return next_round(labels, predictions, weights)


def next_round(labels, predictions, weights):
    """One round: the error, the classifier weight and the new data weights."""
    error = sum(weight for weight, label, guess
                in zip(weights, labels, predictions) if label != guess)
    factor = alpha(error)
    updated = []
    for weight, label, guess in zip(weights, labels, predictions):
        updated.append(weight * math.exp(factor) if label != guess else weight)
    total = sum(updated)
    return {"error": error, "alpha": factor,
            "weights": [value / total for value in updated]}


def ensemble(rounds):
    """The combined prediction: the sign of the weighted vote."""
    size = len(rounds[0][1])
    result = []
    for index in range(size):
        total = sum(weight * predictions[index] for weight, predictions in rounds)
        result.append(1 if total >= 0 else -1)
    return result


def weighted_error(labels, predictions, weights):
    """The error a classifier makes under the given weights."""
    return sum(weight for weight, label, guess
               in zip(weights, labels, predictions) if label != guess)
