"""Principal components: the directions the data actually varies in.

The first component is the direction of greatest variance, the second is the
best direction perpendicular to it, and so on. Projecting onto the first few
keeps most of the variance and drops the rest, which is how a measurement in
four dimensions becomes a picture in two.

The components are eigenvectors of the covariance matrix, computed here by
power iteration with deflation so the module depends on nothing.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "data-exploration", "real-datasets"))
import real_datasets


def _centre(points):
    """The points shifted so that each coordinate has mean zero."""
    dimensions = len(points[0])
    means = [sum(point[index] for point in points) / len(points)
             for index in range(dimensions)]
    return [[value - mean for value, mean in zip(point, means)]
            for point in points]


def _covariance(points):
    """The covariance matrix of the centred points."""
    centred = _centre(points)
    dimensions = len(centred[0])
    size = len(centred)
    return [[sum(row[first] * row[second] for row in centred) / (size - 1)
             for second in range(dimensions)] for first in range(dimensions)]


def components(points, count):
    """The leading directions, by power iteration with deflation."""
    matrix = _covariance(points)
    dimensions = len(matrix)
    found = []
    for _ in range(count):
        vector = [1.0] + [0.0] * (dimensions - 1)
        for _ in range(500):
            product = [sum(matrix[row][column] * vector[column]
                           for column in range(dimensions))
                       for row in range(dimensions)]
            norm = sum(value ** 2 for value in product) ** 0.5
            if norm == 0:
                break
            following = [value / norm for value in product]
            if all(abs(a - b) < 1e-12 for a, b in zip(following, vector)):
                vector = following
                break
            vector = following
        found.append(vector)
        value = sum(vector[row] * sum(matrix[row][column] * vector[column]
                                      for column in range(dimensions))
                    for row in range(dimensions))
        matrix = [[matrix[row][column] - value * vector[row] * vector[column]
                   for column in range(dimensions)] for row in range(dimensions)]
    return found


def explained_variance(points):
    """The share of the variance each component accounts for."""
    matrix = _covariance(points)
    dimensions = len(matrix)
    total = sum(matrix[index][index] for index in range(dimensions))
    directions = components(points, dimensions)
    original = _covariance(points)
    shares = []
    for vector in directions:
        value = sum(vector[row] * sum(original[row][column] * vector[column]
                                      for column in range(dimensions))
                    for row in range(dimensions))
        shares.append(value / total if total else 0.0)
    return shares


def project(points, count):
    """The coordinates of the points in the leading components."""
    directions = components(points, count)
    centred = _centre(points)
    return [[sum(value * component for value, component in zip(row, direction))
             for direction in directions] for row in centred]


def standardise(points):
    """The points scaled so every coordinate has variance one."""
    dimensions = len(points[0])
    means = [sum(point[index] for point in points) / len(points)
             for index in range(dimensions)]
    deviations = []
    for index in range(dimensions):
        variance = sum((point[index] - means[index]) ** 2
                       for point in points) / (len(points) - 1)
        deviations.append(variance ** 0.5 or 1.0)
    return [[(value - mean) / deviation for value, mean, deviation
             in zip(point, means, deviations)] for point in points]


def penguin_reduction(scaled=False):
    """The four penguin measurements reduced to two components.

    Without scaling the answer is meaningless. Body mass is measured in
    grams and runs into the thousands while the bill is measured in
    millimetres and runs into the tens, so the first component is body mass
    and it explains essentially all of the variance. Standardising first
    gives every measurement the same weight, and the two leading components
    then keep about 90 percent.
    """
    rows = real_datasets.rows()
    points = [[float(row["bill_length_mm"]), float(row["bill_depth_mm"]),
               float(row["flipper_length_mm"]), float(row["body_mass_g"])]
              for row in rows]
    if scaled:
        points = standardise(points)
    shares = explained_variance(points)
    return {"components": 2, "variance kept": sum(shares[:2]),
            "first component": shares[0], "shares": shares}
