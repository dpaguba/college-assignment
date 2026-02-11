"""Fitts' law: how long it takes to point at something.

The one quantitative law in interface design. The time to move to a target
depends on the distance to it and its size, and only through their ratio:

    MT = a + b * log2(D / W + 1)

The logarithm is the interesting part. Doubling the distance costs the same as
halving the target, and both cost less than proportionally, because pointing is
a sequence of corrective movements each of which closes a fixed fraction of the
remaining gap.

Everything a designer can do about pointing follows from the formula: make
targets bigger, put them closer, or make them effectively infinite by putting
them against a screen edge.
"""

from __future__ import annotations

import math


def index_of_difficulty(distance, width, form="shannon", edge=False):
    """How hard a pointing task is, in bits.

    The Shannon form adds one inside the logarithm, which keeps the index
    non-negative for targets that are wider than they are far. The original
    1954 form, `log2(2D / W)`, goes negative there, and a negative difficulty
    is not a statement about pointing but about the formula being extrapolated
    past where it was fitted.

    An `edge` target is one against the border of the screen, which the cursor
    cannot overshoot. It behaves as if it extended off-screen, so its effective
    width is far larger than its visible width.
    """
    if distance <= 0:
        return 0.0

    if edge:
        width = width + distance

    if form == "original":
        return math.log2(2 * distance / width)

    return math.log2(distance / width + 1)


def movement_time(distance, width, a=0.23, b=0.16, form="shannon", edge=False):
    """Predicted time in seconds for one pointing movement.

    `a` is the fixed cost of starting and stopping, `b` the cost per bit of
    difficulty. Both are empirical and device-specific: a mouse, a touchscreen
    and a head-mounted cursor have different constants, and comparing devices
    means comparing their fitted `b`, not their raw times.
    """
    return a + b * index_of_difficulty(distance, width, form, edge)


def throughput(difficulty, time):
    """Bits per second, the device-independent measure of pointing performance.

    Reporting a mean time is useless for comparing devices, because it depends
    on which targets were tested. Dividing by the difficulty removes that,
    which is what makes throughput the number that appears in the standard.
    """
    return difficulty / time


def fit(trials):
    """Least squares fit of `a` and `b` to measured trials.

    Each trial is a distance, a width and an observed time. The fit is linear
    because the law is affine in the index of difficulty, so there is a closed
    form and no iteration.

    The returned `r_squared` is what says whether the law applies at all. In
    published studies it is routinely above 0.9, which is unusually good for a
    behavioural model and the reason the law is taken seriously.
    """
    points = [(index_of_difficulty(distance, width), time)
              for distance, width, time in trials]

    n = len(points)
    mean_x = sum(x for x, _ in points) / n
    mean_y = sum(y for _, y in points) / n

    covariance = sum((x - mean_x) * (y - mean_y) for x, y in points)
    variance = sum((x - mean_x) ** 2 for x, _ in points)

    slope = covariance / variance if variance else 0.0
    intercept = mean_y - slope * mean_x

    residual = sum((y - (intercept + slope * x)) ** 2 for x, y in points)
    total = sum((y - mean_y) ** 2 for _, y in points)
    r_squared = 1.0 if total == 0 else 1 - residual / total

    return intercept, slope, r_squared


def effective_width(endpoints):
    """Target width implied by how the endpoints actually scattered.

    The nominal width is what the designer drew; the effective width is what
    the user treated it as. Taking `4.133` standard deviations of the endpoint
    spread makes 96% of the hits fall inside it, which normalises for how
    carefully the participant was aiming.

    Without this adjustment a participant who trades accuracy for speed looks
    faster rather than less accurate, and the fitted throughput is wrong in
    their favour.
    """
    return 4.133 * _standard_deviation(endpoints)


def _standard_deviation(values):
    """Sample standard deviation."""
    n = len(values)
    if n < 2:
        return 0.0
    mean = sum(values) / n
    return math.sqrt(sum((value - mean) ** 2 for value in values) / (n - 1))


def effective_difficulty(distance, endpoints):
    """Index of difficulty computed from the effective rather than nominal width."""
    return index_of_difficulty(distance, effective_width(endpoints))


def compare_layouts(layouts, a=0.23, b=0.16):
    """Predicted times for several target layouts, for design decisions.

    Each layout is a name and a list of distance and width pairs, one per
    target the user has to reach. Summing the predicted times turns a question
    about menu design into arithmetic.
    """
    return {name: sum(movement_time(distance, width, a, b)
                      for distance, width in targets)
            for name, targets in layouts.items()}
