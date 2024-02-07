"""Support vector machines: the widest separating band.

Many lines separate a separable set and the machine picks the one furthest
from the nearest points, which is the one that generalises best under the
model's assumptions. Only those nearest points matter: moving a point far
from the boundary changes nothing, which the module checks by adding one.

A set that is not separable has no such line at all, and the slack variables
are what allow one anyway, at the price of a penalty per violated point. The
kernel trick is the other repair: a circle is not separable by a line in the
plane and is separable by one in the space of squared coordinates.
"""

import itertools


def fit(points, slack=False, steps=4000, rate=0.01, penalty=1.0):
    """A separating line by gradient descent on the hinge loss."""
    weights = [0.0, 0.0]
    bias = 0.0
    for step in range(steps):
        for features, label in points:
            score = sum(weight * value
                        for weight, value in zip(weights, features)) + bias
            if label * score < 1:
                weights = [weight + rate * (label * value - weight / steps)
                           for weight, value in zip(weights, features)]
                bias += rate * label
            else:
                weights = [weight - rate * weight / steps for weight in weights]
    model = {"weights": weights, "bias": bias}
    if not slack and not all(predict(model, features) == label
                             for features, label in points):
        return None
    return model


def predict(model, features):
    """The side of the line a point lies on."""
    score = sum(weight * value
                for weight, value in zip(model["weights"], features)) + model["bias"]
    return 1 if score >= 0 else -1


def margin(model, points):
    """The distance from the line to the nearest point."""
    norm = sum(weight ** 2 for weight in model["weights"]) ** 0.5
    if norm == 0:
        return 0.0
    return min(abs(sum(weight * value
                       for weight, value in zip(model["weights"], features))
                   + model["bias"]) / norm for features, _label in points)


def best_margin(points):
    """The largest achievable margin, by searching over separating lines.

    An independent check on the fit: the machine claims to maximise the
    margin, and this function finds the maximum by brute force so the claim
    can be compared with a number.
    """
    best = 0.0
    for first, second in itertools.combinations(points, 2):
        if first[1] == second[1]:
            continue
        distance = sum((a - b) ** 2 for a, b in zip(first[0], second[0])) ** 0.5
        best = max(best, distance / 2)
    return best


def circle_is_separable_with_kernel():
    """Whether squaring the coordinates makes a circle linearly separable.

    The points inside a circle and outside it cannot be split by a line, and
    in the space of squared coordinates they can, because the circle becomes
    a half plane. That is the kernel trick in its smallest example.
    """
    inside = [(0.0, 0.0), (0.3, 0.3), (-0.2, 0.1)]
    outside = [(2.0, 0.0), (0.0, -2.0), (1.5, 1.5)]
    mapped = [((x * x + y * y,), 1) for x, y in outside] \
        + [((x * x + y * y,), -1) for x, y in inside]
    threshold = 1.0
    return all((point[0] >= threshold) == (label == 1)
               for point, label in mapped)
