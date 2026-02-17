"""Projections: from a 3D scene to a 2D image plane.

Two families, and the difference is one row of the matrix. Parallel projection
keeps `w` at 1, so the size of an object does not depend on its distance.
Perspective projection writes the depth into `w`, and the division that follows
shrinks distant objects. Everything else, the clipping, the rasterising, the
depth test, is identical for both.

The output is normalised device coordinates, the cube from -1 to 1 in every
axis, which is what the clipper and the viewport transform expect.
"""

from __future__ import annotations

import math


def identity():
    """The 4x4 identity."""
    return [[1.0 if row == column else 0.0 for column in range(4)] for row in range(4)]


def orthographic(left, right, bottom, top, near, far):
    """Parallel projection: map an axis-aligned box to the unit cube.

    Nothing is foreshortened, so parallel lines stay parallel and lengths stay
    comparable. That is exactly why CAD and technical drawings use it, and
    exactly why it looks unnatural.
    """
    matrix = identity()
    matrix[0][0], matrix[0][3] = 2 / (right - left), -(right + left) / (right - left)
    matrix[1][1], matrix[1][3] = 2 / (top - bottom), -(top + bottom) / (top - bottom)
    matrix[2][2], matrix[2][3] = -2 / (far - near), -(far + near) / (far - near)
    return matrix


def frustum(left, right, bottom, top, near, far):
    """Perspective projection from the six planes of a viewing frustum.

    The third row is the whole trick: it copies `-z` into `w`, so the divide
    that follows scales x and y by the reciprocal of the distance. The
    remaining entries are chosen so that the near plane lands on -1 and the far
    plane on +1 after that same divide.
    """
    matrix = [[0.0] * 4 for _ in range(4)]
    matrix[0][0], matrix[0][2] = 2 * near / (right - left), (right + left) / (right - left)
    matrix[1][1], matrix[1][2] = 2 * near / (top - bottom), (top + bottom) / (top - bottom)
    matrix[2][2], matrix[2][3] = -(far + near) / (far - near), -2 * far * near / (far - near)
    matrix[3][2] = -1.0
    return matrix


def perspective(fov_y, aspect, near, far):
    """Perspective projection from a field of view, the usual way to state it.

    A symmetric frustum, so it needs four numbers instead of six. `fov_y` is
    the **full** vertical angle in radians, hence the half angle in the tangent.
    """
    top = near * math.tan(fov_y / 2)
    right = top * aspect
    return frustum(-right, right, -top, top, near, far)


def viewport(x, y, width, height):
    """Map normalised device coordinates to pixels.

    The y axis is flipped, because device coordinates go up and image rows go
    down. Getting this wrong produces an upside-down image and nothing else,
    which is why it is such a common bug.
    """
    matrix = identity()
    matrix[0][0], matrix[0][3] = width / 2, x + width / 2
    matrix[1][1], matrix[1][3] = -height / 2, y + height / 2
    matrix[2][2], matrix[2][3] = 0.5, 0.5
    return matrix


def project(matrix, point):
    """Apply a projection and divide by `w`, returning the point and its `w`.

    `w` is returned because it is needed twice more downstream: the clipper
    works on the unprojected coordinates and needs to know the sign, and
    perspective-correct interpolation needs `1/w` per vertex.
    """
    x, y, z = point
    coordinates = [sum(matrix[row][column] * value
                       for column, value in enumerate((x, y, z, 1.0)))
                   for row in range(4)]
    w = coordinates[3]
    if abs(w) < 1e-12:
        return tuple(coordinates[:3]), w
    return tuple(value / w for value in coordinates[:3]), w


def depth_precision(near, far, samples=8):
    """Where the depth buffer's resolution actually goes.

    After the perspective divide, depth is a function of `1/z`, so almost all
    the available precision sits near the near plane. The function reports, for
    evenly spaced world depths, the normalised depth each maps to; the gaps
    between the first few are enormous and between the last few are negligible.

    This is the reason for depth fighting on distant coplanar surfaces, and the
    reason that pushing the near plane closer is far more damaging than pulling
    the far plane further away.
    """
    result = []
    for index in range(samples + 1):
        z = near + (far - near) * index / samples
        ndc = ((far + near) / (far - near) * z - 2 * far * near / (far - near)) / z
        result.append((z, ndc))
    return result


def field_of_view(near, top):
    """Recover the full vertical field of view from a frustum."""
    return 2 * math.atan(top / near)


def is_visible(point, near, far):
    """Whether a camera-space point lies between the near and far planes.

    The camera looks down negative z, so a visible point has negative z and the
    test reads backwards from the intuition.
    """
    return -far <= point[2] <= -near
