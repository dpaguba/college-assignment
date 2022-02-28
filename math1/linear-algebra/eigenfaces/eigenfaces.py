"""Eigenfaces: the application the lecture closes the linear algebra with.

Faces are points in a space of one dimension per pixel, and the principal
components are the directions in which the sample varies most. Those
directions are the eigenvectors of the covariance matrix, so the whole
construction is the eigenvalue chapter applied to data, and the number of
components needed is a measurement rather than a choice.
"""

import numpy


def sample_faces(count=8, size=6):
    """A small synthetic set of face-like images, as flattened rows.

    Built from a handful of patterns so that the data has genuine structure:
    the images lie close to a low-dimensional subspace, which is the property
    the method exploits and the reason a real face database works at all.
    """
    generator = numpy.random.default_rng(7)
    patterns = numpy.array([
        [1.0 if (row - size / 2) ** 2 + (column - size / 2) ** 2 < 4 else 0.0
         for row in range(size) for column in range(size)],
        [1.0 if row < size / 2 else 0.0
         for row in range(size) for column in range(size)],
        [1.0 if column % 2 == 0 else 0.0
         for row in range(size) for column in range(size)]])
    weights = generator.random((count, len(patterns)))
    data = weights @ patterns
    data += 0.01 * generator.standard_normal(data.shape)
    return data


def principal_components(data, count):
    """The directions of greatest variance, as rows."""
    centred = data - data.mean(axis=0)
    _, _, directions = numpy.linalg.svd(centred, full_matrices=False)
    return directions[:count]


def are_orthonormal(components, tolerance=1e-9):
    """Whether the components are perpendicular and of length one."""
    product = components @ components.T
    return bool(numpy.allclose(product, numpy.eye(len(components)),
                               atol=tolerance))


def reconstruct(data, count):
    """The data projected onto the leading components and back."""
    mean = data.mean(axis=0)
    centred = data - mean
    components = principal_components(data, count)
    return mean + (centred @ components.T) @ components


def reconstruction_error(data, count):
    """The mean squared error of the reconstruction."""
    return float(numpy.mean((data - reconstruct(data, count)) ** 2))


def explained_variance(data):
    """The share of the variance each component accounts for."""
    centred = data - data.mean(axis=0)
    _, values, _ = numpy.linalg.svd(centred, full_matrices=False)
    squares = values ** 2
    return squares / squares.sum()


def nearest_neighbour_works(data, components):
    """Whether every face is closest to itself in the reduced coordinates.

    The recognition step: a face is described by its coordinates in the
    component basis, and a new image is matched to the nearest stored one.
    Checking that each stored face matches itself is the weakest form of the
    test and the one that fails first if the projection loses too much.
    """
    mean = data.mean(axis=0)
    directions = principal_components(data, components)
    coordinates = (data - mean) @ directions.T
    for index, point in enumerate(coordinates):
        distances = numpy.linalg.norm(coordinates - point, axis=1)
        if int(numpy.argmin(distances)) != index:
            return False
    return True
