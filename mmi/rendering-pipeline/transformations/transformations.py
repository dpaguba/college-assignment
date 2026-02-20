"""Affine transformations in homogeneous coordinates.

A 3D point gets a fourth coordinate `w`, and every transformation becomes a
4x4 matrix. The payoff is that translation, which is not linear in 3D, becomes
linear in 4D, so the whole chain of model, view and projection transforms
collapses into a single matrix multiplication per vertex.

The convention here is column vectors with the matrix on the left, so
`translate(a) @ rotate(b)` rotates first and then translates. Reading a chain
right to left gives the order the operations actually happen in.
"""

from __future__ import annotations

import math


def identity():
    """The 4x4 identity, the neutral element of the transformation group."""
    return [[1.0 if row == column else 0.0 for column in range(4)] for row in range(4)]


def multiply(first, second):
    """Matrix product, applying `second` before `first`."""
    return [[sum(first[row][k] * second[k][column] for k in range(4))
             for column in range(4)] for row in range(4)]


def compose(*matrices):
    """Fold a chain of transformations into one matrix, leftmost applied last."""
    result = identity()
    for matrix in matrices:
        result = multiply(result, matrix)
    return result


def apply(matrix, point):
    """Transform a point, dividing by `w` so the result is a 3D point again.

    The division is what makes the perspective transform work: an affine matrix
    leaves `w` at 1 and the division is a no-op, while a projection matrix puts
    the depth into `w` and the division performs the foreshortening.
    """
    x, y, z = point
    coordinates = [sum(matrix[row][column] * value
                       for column, value in enumerate((x, y, z, 1.0)))
                   for row in range(4)]
    w = coordinates[3]
    if abs(w) < 1e-12:
        return tuple(coordinates[:3])
    return tuple(value / w for value in coordinates[:3])


def apply_direction(matrix, vector):
    """Transform a direction, ignoring translation by setting `w` to zero.

    Directions have no position, so translating them is meaningless. This is
    exactly what the fourth coordinate is for: `w = 1` marks a point, `w = 0`
    marks a direction, and the same matrix does the right thing for both.
    """
    x, y, z = vector
    return tuple(sum(matrix[row][column] * value
                     for column, value in enumerate((x, y, z, 0.0)))
                 for row in range(3))


def translate(dx, dy, dz):
    """Move by a vector."""
    matrix = identity()
    matrix[0][3], matrix[1][3], matrix[2][3] = float(dx), float(dy), float(dz)
    return matrix


def scale(sx, sy=None, sz=None):
    """Scale about the origin, uniformly if only one factor is given."""
    if sy is None:
        sy = sz = sx
    matrix = identity()
    matrix[0][0], matrix[1][1], matrix[2][2] = float(sx), float(sy), float(sz)
    return matrix


def rotate_x(angle):
    """Rotate about the x axis, angle in radians, counterclockwise."""
    c, s = math.cos(angle), math.sin(angle)
    matrix = identity()
    matrix[1][1], matrix[1][2] = c, -s
    matrix[2][1], matrix[2][2] = s, c
    return matrix


def rotate_y(angle):
    """Rotate about the y axis.

    The signs are the mirror image of the other two axes, because the cyclic
    order of the axes is x, y, z and the y rotation moves z towards x.
    """
    c, s = math.cos(angle), math.sin(angle)
    matrix = identity()
    matrix[0][0], matrix[0][2] = c, s
    matrix[2][0], matrix[2][2] = -s, c
    return matrix


def rotate_z(angle):
    """Rotate about the z axis, the familiar 2D rotation lifted into 3D."""
    c, s = math.cos(angle), math.sin(angle)
    matrix = identity()
    matrix[0][0], matrix[0][1] = c, -s
    matrix[1][0], matrix[1][1] = s, c
    return matrix


def rotate_axis(axis, angle):
    """Rotate about an arbitrary axis through the origin (Rodrigues' formula).

    Decomposing this into three axis rotations is possible but gives gimbal
    lock and a different result depending on the order chosen. One rotation
    about one axis has neither problem, which is also the argument for
    quaternions.
    """
    length = math.sqrt(sum(component * component for component in axis))
    x, y, z = (component / length for component in axis)
    c, s = math.cos(angle), math.sin(angle)
    t = 1 - c

    matrix = identity()
    matrix[0][0], matrix[0][1], matrix[0][2] = t*x*x + c, t*x*y - s*z, t*x*z + s*y
    matrix[1][0], matrix[1][1], matrix[1][2] = t*x*y + s*z, t*y*y + c, t*y*z - s*x
    matrix[2][0], matrix[2][1], matrix[2][2] = t*x*z - s*y, t*y*z + s*x, t*z*z + c
    return matrix


def rotate_about(point, axis, angle):
    """Rotate about an axis through an arbitrary point.

    Move the point to the origin, rotate, move back. The pattern generalises:
    any transformation about a place is the transformation conjugated by a
    translation to that place.
    """
    x, y, z = point
    return compose(translate(x, y, z), rotate_axis(axis, angle), translate(-x, -y, -z))


def shear(xy=0.0, xz=0.0, yx=0.0, yz=0.0, zx=0.0, zy=0.0):
    """Shear, where each factor names the coordinate it adds to which axis."""
    matrix = identity()
    matrix[0][1], matrix[0][2] = xy, xz
    matrix[1][0], matrix[1][2] = yx, yz
    matrix[2][0], matrix[2][1] = zx, zy
    return matrix


def transpose(matrix):
    """Swap rows and columns."""
    return [[matrix[column][row] for column in range(4)] for row in range(4)]


def inverse(matrix):
    """Invert a 4x4 matrix by Gauss-Jordan elimination with partial pivoting."""
    size = 4
    working = [list(row) + [1.0 if row_index == column else 0.0 for column in range(size)]
               for row_index, row in enumerate(matrix)]

    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(working[row][column]))
        if abs(working[pivot][column]) < 1e-12:
            raise ValueError("matrix is singular")
        working[column], working[pivot] = working[pivot], working[column]

        divisor = working[column][column]
        working[column] = [value / divisor for value in working[column]]

        for row in range(size):
            if row != column and working[row][column] != 0.0:
                factor = working[row][column]
                working[row] = [value - factor * other
                                for value, other in zip(working[row], working[column])]

    return [row[size:] for row in working]


def normal_matrix(matrix):
    """The matrix that transforms normals: the inverse transpose.

    Normals are not directions in the ordinary sense, they are defined by being
    perpendicular to the surface. Under a non-uniform scale the surface tilts
    one way and a naively transformed normal tilts the other, so lighting comes
    out wrong on any squashed object. The inverse transpose preserves the
    perpendicularity, which is the property that actually matters.
    """
    return transpose(inverse(matrix))


def look_at(eye, target, up):
    """The view matrix: move the world so the camera sits at the origin.

    The camera looks down its own negative z axis, by the OpenGL convention.
    The matrix is the inverse of the camera's placement in the world, which for
    a rigid motion is the transposed rotation plus a negated translation, so it
    can be written down directly without an inversion.
    """
    forward = _normalise(_subtract(target, eye))
    right = _normalise(_cross(forward, up))
    true_up = _cross(right, forward)

    matrix = identity()
    matrix[0][:3] = list(right)
    matrix[1][:3] = list(true_up)
    matrix[2][:3] = [-component for component in forward]
    matrix[0][3] = -_dot(right, eye)
    matrix[1][3] = -_dot(true_up, eye)
    matrix[2][3] = _dot(forward, eye)
    return matrix


def _subtract(a, b):
    """Componentwise difference of two 3-vectors."""
    return tuple(x - y for x, y in zip(a, b))


def _dot(a, b):
    """Dot product of two 3-vectors."""
    return sum(x * y for x, y in zip(a, b))


def _cross(a, b):
    """Cross product of two 3-vectors."""
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])


def _normalise(vector):
    """Scale a vector to unit length."""
    length = math.sqrt(_dot(vector, vector))
    return tuple(component / length for component in vector)
