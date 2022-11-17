"""The confusion matrix, and why accuracy alone is a bad summary.

Four counts, and every measure in the block is a ratio of them. Accuracy is
the diagonal over the total, and on an unbalanced problem it is dominated by
the large class: a classifier that never predicts the rare class reaches 99
percent accuracy and finds nothing, which the module demonstrates with such a
classifier.
"""


def build(truth, predicted):
    """The four counts of a binary classification."""
    counts = {"true positive": 0, "false positive": 0,
              "false negative": 0, "true negative": 0}
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


def accuracy(matrix):
    """The share of correct decisions."""
    total = sum(matrix.values())
    if total == 0:
        return 0.0
    return (matrix["true positive"] + matrix["true negative"]) / total


def unbalanced_example():
    """A classifier that predicts the majority class and looks excellent."""
    truth = [1] * 10 + [0] * 990
    predicted = [0] * 1000
    matrix = build(truth, predicted)
    recall = matrix["true positive"] / (matrix["true positive"]
                                        + matrix["false negative"])
    return {"accuracy": accuracy(matrix), "recall": recall, "matrix": matrix}


def specificity(matrix):
    """The share of the negatives that are recognised."""
    negatives = matrix["true negative"] + matrix["false positive"]
    return matrix["true negative"] / negatives if negatives else 0.0
