"""Precision and recall: two questions that pull against each other.

Precision asks what share of the positive predictions is right, recall what
share of the positive cases is found. Predicting everything positive gives
perfect recall and the base rate as precision, so neither number alone says
anything, and the F measure is the harmonic mean that refuses to be gamed by
either extreme.

The curve is the summary that keeps both: as the threshold falls, recall rises and
precision falls, and where to sit on that curve is a decision about the cost
of each error rather than a property of the model.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "confusion-matrix"))
import confusion_matrix


def precision(matrix):
    """The share of the positive predictions that are correct."""
    predicted = matrix["true positive"] + matrix["false positive"]
    return matrix["true positive"] / predicted if predicted else 0.0


def recall(matrix):
    """The share of the positive cases that are found."""
    actual = matrix["true positive"] + matrix["false negative"]
    return matrix["true positive"] / actual if actual else 0.0


def f_measure(matrix, beta=1.0):
    """The weighted harmonic mean of the two."""
    first, second = precision(matrix), recall(matrix)
    if first + second == 0:
        return 0.0
    weight = beta ** 2
    return (1 + weight) * first * second / (weight * first + second)


def curve(scores=None, truth=None):
    """The precision and recall at every threshold."""
    scores = scores or [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
    truth = truth or [1, 1, 0, 1, 0, 1, 0, 0]
    points = []
    for threshold in sorted(scores, reverse=True):
        predicted = [1 if score >= threshold else 0 for score in scores]
        matrix = confusion_matrix.build(truth, predicted)
        points.append({"threshold": threshold, "precision": precision(matrix),
                       "recall": recall(matrix)})
    return points
