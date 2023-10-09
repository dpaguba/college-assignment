"""Evaluating a classifier that produces scores rather than decisions.

A threshold turns a score into a decision, and every threshold gives a
different confusion matrix. The ROC curve plots all of them, and the area
under it summarises the ranking: it is one when every positive scores above
every negative, one half for a random order, and below one half when the
ranking is inverted.

The area does not depend on the threshold or on any monotone rescaling of the
scores, which is what makes it the measure to report when the operating point
is not yet chosen.
"""


def matrix(truth, predicted):
    """The four counts of a binary decision."""
    counts = {"true positive": 0, "false positive": 0, "false negative": 0,
              "true negative": 0}
    for actual, guess in zip(truth, predicted):
        if actual == 1 and guess == 1:
            counts["true positive"] += 1
        elif actual == 0 and guess == 1:
            counts["false positive"] += 1
        elif actual == 1 and guess == 0:
            counts["false negative"] += 1
        else:
            counts["true negative"] += 1
    return counts


def precision(counts):
    """The share of the positive predictions that are right."""
    predicted = counts["true positive"] + counts["false positive"]
    return counts["true positive"] / predicted if predicted else 0.0


def recall(counts):
    """The share of the positive cases that are found."""
    actual = counts["true positive"] + counts["false negative"]
    return counts["true positive"] / actual if actual else 0.0


def roc(scores, labels):
    """The curve of false positive against true positive rates."""
    order = sorted(range(len(scores)), key=lambda index: -scores[index])
    positives = sum(1 for label in labels if label == 1)
    negatives = len(labels) - positives
    points = [(0.0, 0.0)]
    found, wrong = 0, 0
    for index in order:
        if labels[index] == 1:
            found += 1
        else:
            wrong += 1
        points.append((wrong / negatives if negatives else 0.0,
                       found / positives if positives else 0.0))
    if points[-1] != (1.0, 1.0):
        points.append((1.0, 1.0))
    return points


def auc(scores, labels):
    """The area under the curve, by the trapezium rule."""
    points = roc(scores, labels)
    total = 0.0
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        total += (x2 - x1) * (y1 + y2) / 2
    return total
