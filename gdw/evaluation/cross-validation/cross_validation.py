"""Cross validation: testing on data the model has not seen.

Testing on the training data measures how well a model remembers, not how
well it predicts, and the difference grows with the flexibility of the model.
Splitting into folds and testing each one against a model trained on the rest
uses every observation exactly once for testing, which is what makes it worth
the extra fits.

More folds mean more training data per fit and therefore less variability in
the estimate, at the cost of more fits: leaving one out is the extreme of
both.
"""

import random


def split(items, folds):
    """The training and test parts of each fold."""
    size = len(items)
    result = []
    for index in range(folds):
        test = [item for position, item in enumerate(items)
                if position % folds == index]
        train = [item for position, item in enumerate(items)
                 if position % folds != index]
        result.append((train, test))
    return result


def variability(seed=0, repeats=40, size=60):
    """How much the estimate moves between repetitions, by number of folds."""
    generator = random.Random(seed)
    report = {}
    for name, folds in (("two folds", 2), ("ten folds", 10)):
        estimates = []
        for _ in range(repeats):
            data = [(generator.random(), generator.randint(0, 1))
                    for _ in range(size)]
            scores = []
            for train, test in split(data, folds):
                threshold = sum(value for value, _label in train) / len(train)
                correct = sum(1 for value, label in test
                              if (value > threshold) == bool(label))
                scores.append(correct / len(test))
            estimates.append(sum(scores) / len(scores))
        mean = sum(estimates) / len(estimates)
        report[name] = sum((value - mean) ** 2 for value in estimates) \
            / len(estimates)
    return report


def optimism(seed=0, size=40):
    """Training accuracy against the cross validated one on noise.

    A model flexible enough to memorise the training data scores perfectly on
    it and no better than chance on anything else, which is the gap cross
    validation exists to expose.
    """
    generator = random.Random(seed)
    data = [(index, generator.randint(0, 1)) for index in range(size)]
    memory = dict(data)
    training = sum(1 for key, label in data if memory[key] == label) / size
    scores = []
    for train, test in split(data, 5):
        table = dict(train)
        correct = sum(1 for key, label in test if table.get(key, 0) == label)
        scores.append(correct / len(test))
    return {"training accuracy": training,
            "cross validated accuracy": sum(scores) / len(scores)}
