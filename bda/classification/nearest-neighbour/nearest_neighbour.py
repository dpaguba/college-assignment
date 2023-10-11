"""The nearest neighbour classifier: no model, all the work at prediction time.

Training is storing the data. Predicting is finding the closest examples and
taking their majority label, so the cost moves entirely to the query and the
method has no parameters to fit, only k and a distance.

The distance is where the assumptions hide. A feature measured in grams
dominates one measured in millimetres, so scaling changes the neighbours and
therefore the answer, which the module demonstrates on a pair of features
differing by three orders of magnitude.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "data-exploration", "real-datasets"))
import real_datasets


def _distance(first, second):
    """The Euclidean distance."""
    return sum((a - b) ** 2 for a, b in zip(first, second)) ** 0.5


def classify(training, point, k=1):
    """The majority label among the k nearest examples."""
    ordered = sorted(training, key=lambda item: _distance(item[0], point))
    labels = [label for _features, label in ordered[:k]]
    return max(set(labels), key=labels.count)


def cost(training_size, dimensions):
    """Where the work happens: nothing at training, everything at prediction."""
    return {"training": 0, "prediction": training_size * dimensions,
            "memory": training_size * dimensions}


def penguin_accuracy(k=3):
    """Leave-one-out accuracy on the penguin sample, using two measurements.

    The bill length and depth separate the three species well enough for a
    nearest neighbour rule, which is the point of the example: no model is
    fitted and the geometry of the data does the work.
    """
    rows = real_datasets.rows()
    data = [((float(row["bill_length_mm"]), float(row["bill_depth_mm"])),
             row["species"]) for row in rows]
    correct = 0
    for index, (point, label) in enumerate(data):
        rest = data[:index] + data[index + 1:]
        if classify(rest, point, k) == label:
            correct += 1
    return {"accuracy": correct / len(data), "size": len(data)}
