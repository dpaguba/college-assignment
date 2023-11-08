"""Bagging: averaging away the variance and none of the bias.

Draw bootstrap samples, fit a model to each, average the predictions. Each
model sees a sample of the same size drawn with replacement, so about a third
of the data is left out of each one, which the module measures and which is
what makes the out-of-bag estimate possible.

Averaging lowers the variance and leaves the bias where it was, so bagging
helps an unstable model such as a deep tree and does nothing for a stable one
such as a linear fit.
"""

import math
import random


def bootstrap(items, seed=0):
    """A sample of the same size, drawn with replacement."""
    generator = random.Random(seed)
    return [generator.choice(items) for _ in items]


def out_of_bag_share(size, seed=0, repeats=200):
    """The share of the data left out of a bootstrap sample.

    It approaches one over e, because each item is missed with probability
    one minus one over n, n times. The module measures it rather than quoting
    it.
    """
    generator = random.Random(seed)
    total = 0.0
    items = list(range(size))
    for _ in range(repeats):
        drawn = {generator.choice(items) for _ in items}
        total += (size - len(drawn)) / size
    return total / repeats


def variance_reduction(seed=0, samples=200, learners=25):
    """The bias and variance of one model against an average of many."""
    generator = random.Random(seed)
    truth = 3.0
    single, ensemble = [], []
    for _ in range(samples):
        data = [truth + generator.gauss(0, 1.0) for _ in range(10)]
        single.append(sum(data) / len(data))
        predictions = []
        for index in range(learners):
            sample = [generator.choice(data) for _ in data]
            predictions.append(sum(sample) / len(sample))
        ensemble.append(sum(predictions) / len(predictions))
    return {"single bias": sum(single) / len(single) - truth,
            "ensemble bias": sum(ensemble) / len(ensemble) - truth,
            "single variance": _variance(single),
            "ensemble variance": _variance(ensemble)}


def _variance(values):
    """The variance of a list."""
    mean = sum(values) / len(values)
    return sum((value - mean) ** 2 for value in values) / len(values)
