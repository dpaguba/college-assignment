"""What makes a deep network trainable, measured on small examples.

Four problems and their standard answers. A saturating activation loses the
gradient with depth, and a rectifier does not. Features on different scales
make the descent zigzag, and normalising them removes it. A learning rate
above the curvature diverges. And a network large enough to fit the data
fits the noise, which dropout and early stopping both address.
"""


def gradient_share(activation, depth):
    """How much of the gradient survives a stack of that depth."""
    factors = {"sigmoid": 0.25, "tanh": 1.0, "relu": 1.0}
    if activation not in factors:
        raise ValueError("unknown activation: %s" % activation)
    return factors[activation] ** depth


def normalisation_effect(steps=2000, rate=0.02):
    """How many steps a descent needs with and without normalised inputs."""
    raw = _descend([(1.0, 1000.0)], rate, steps)
    normalised = _descend([(1.0, 1.0)], rate, steps)
    return {"raw steps": raw, "normalised steps": normalised}


def _descend(scales, rate, steps):
    """Steps until a quadratic with the given curvatures is minimised."""
    position = [1.0 for _ in scales[0]]
    curvature = scales[0]
    for step in range(1, steps + 1):
        gradient = [2 * value * scale
                    for value, scale in zip(position, curvature)]
        position = [value - rate * component / max(curvature)
                    for value, component in zip(position, gradient)]
        if all(abs(value) < 1e-3 for value in position):
            return step
    return steps


def diverges(rate, curvature=2.0, steps=100):
    """Whether gradient descent runs away at the given learning rate."""
    position = 1.0
    for _ in range(steps):
        position -= rate * curvature * position
        if abs(position) > 1e6:
            return True
    return False


def dropout_effect(seed=0, size=200):
    """The gap between training and test accuracy with and without dropout.

    Modelled by adding noise to the features during training, which is what
    dropout does to the activations: the network cannot rely on any single
    input and generalises better.
    """
    import random
    generator = random.Random(seed)
    data = [((generator.random(), generator.random()),
             1 if generator.random() < 0.5 else 0) for _ in range(size)]
    train, test = data[:size // 2], data[size // 2:]
    without = _gap(train, test, noise=0.0, generator=generator)
    with_dropout = _gap(train, test, noise=0.4, generator=generator)
    return {"without dropout": without, "with dropout": with_dropout}


def _gap(train, test, noise, generator):
    """The difference between training and test accuracy of a memoriser."""
    table = {}
    for features, label in train:
        key = tuple(round(value + (generator.random() - 0.5) * noise, 1)
                    for value in features)
        table[key] = label
    def accuracy(rows):
        """The share the lookup gets right."""
        correct = 0
        for features, label in rows:
            key = tuple(round(value, 1) for value in features)
            correct += int(table.get(key, 0) == label)
        return correct / len(rows)
    return accuracy(train) - accuracy(test)


def early_stopping(validation_errors):
    """The epoch before the validation error starts rising."""
    best = min(validation_errors)
    return {"epoch": validation_errors.index(best), "error": best}
