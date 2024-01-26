"""The decomposition, measured rather than derived.

The expected error of a model splits into three terms: the squared bias, how
far the average prediction sits from the truth; the variance, how much the
prediction moves between training sets; and the noise, which no model can
remove. A simple model has high bias and low variance and a complex one the
opposite, so the total has a minimum somewhere in between.

The module fits polynomials of several degrees to many samples of a noisy
function and reports all three terms, so the decomposition can be seen rather
than believed.
"""

import random


def _truth(point):
    """The function the models are trying to recover."""
    return point ** 2 - 0.5 * point


def decompose(degree, seed=0, samples=200, size=12, noise=0.3):
    """The three terms of the error at a fixed test point."""
    generator = random.Random(seed)
    test_point = 0.5
    predictions = []
    for _ in range(samples):
        xs = [generator.uniform(-1, 1) for _ in range(size)]
        ys = [_truth(x) + generator.gauss(0, noise) for x in xs]
        coefficients = _fit(xs, ys, degree)
        predictions.append(_evaluate(coefficients, test_point))
    average = sum(predictions) / len(predictions)
    variance = sum((value - average) ** 2 for value in predictions) \
        / len(predictions)
    bias = (average - _truth(test_point)) ** 2
    return {"bias squared": bias, "variance": variance,
            "noise": noise ** 2, "error": bias + variance + noise ** 2}


def _fit(xs, ys, degree):
    """A least squares polynomial fit by the normal equations."""
    size = degree + 1
    matrix = [[sum(x ** (row + column) for x in xs) for column in range(size)]
              for row in range(size)]
    vector = [sum(y * x ** row for x, y in zip(xs, ys)) for row in range(size)]
    return _solve(matrix, vector)


def _solve(matrix, vector):
    """Gaussian elimination with partial pivoting."""
    size = len(vector)
    rows = [list(row) + [value] for row, value in zip(matrix, vector)]
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(rows[row][column]))
        rows[column], rows[pivot] = rows[pivot], rows[column]
        if abs(rows[column][column]) < 1e-12:
            continue
        divisor = rows[column][column]
        rows[column] = [value / divisor for value in rows[column]]
        for row in range(size):
            if row == column:
                continue
            factor = rows[row][column]
            rows[row] = [value - factor * other
                         for value, other in zip(rows[row], rows[column])]
    return [row[-1] for row in rows]


def _evaluate(coefficients, point):
    """The value of a polynomial."""
    return sum(coefficient * point ** power
               for power, coefficient in enumerate(coefficients))
