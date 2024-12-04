"""Marching squares: extracting a contour from a sampled scalar field.

The field is known only at grid points. The contour at a chosen level runs
between them, and the algorithm reconstructs it cell by cell: classify the four
corners as above or below the level, look up which edges the contour crosses,
and interpolate where along each edge it crosses.

Sixteen corner patterns, and the table is the whole algorithm. Two of them are
ambiguous, and that ambiguity is not a flaw in the method but a genuine
consequence of not knowing what the field does between the samples.
"""

from __future__ import annotations

CASES = {
    0: [], 15: [],
    1: [(0, 3)], 14: [(0, 3)],
    2: [(0, 1)], 13: [(0, 1)],
    3: [(1, 3)], 12: [(1, 3)],
    4: [(1, 2)], 11: [(1, 2)],
    6: [(0, 2)], 9: [(0, 2)],
    7: [(2, 3)], 8: [(2, 3)],
    5: [(0, 3), (1, 2)],
    10: [(0, 1), (2, 3)],
}
"""Which cell edges the contour connects, per corner pattern.

Corners are numbered bottom-left, bottom-right, top-right, top-left, one bit
each, and edge `e` is the one between corner `e` and corner `e+1`: 0 bottom,
1 right, 2 top, 3 left.

A code and its complement give the same segments, since swapping which side is
"above" does not move the boundary between them. Cases 5 and 10 are the
saddles, the two patterns with opposite corners above and the others below,
where two different pairings are equally consistent with the samples.
"""


def corner_code(values, level):
    """Four bits, one per corner, set when that corner is above the level.

    The order is bottom-left, bottom-right, top-right, top-left, which fixes
    the numbering of the case table and nothing else.
    """
    code = 0
    for index, value in enumerate(values):
        if value >= level:
            code |= 1 << index
    return code


def interpolate(a, b, value_a, value_b, level):
    """Where along an edge the contour crosses, by linear interpolation.

    Placing the crossing at the midpoint instead is the difference between a
    contour that looks blocky and one that looks smooth, and it costs one
    division. The linear assumption is exactly the assumption that the field
    is linear between samples, which is the same assumption the whole method
    rests on.
    """
    if abs(value_b - value_a) < 1e-12:
        return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    ratio = (level - value_a) / (value_b - value_a)
    return (a[0] + ratio * (b[0] - a[0]), a[1] + ratio * (b[1] - a[1]))


def contour(field, level=0.0, resolve_saddle=True):
    """All contour segments of a sampled field at one level.

    The output is a set of independent segments, not connected curves. Joining
    them into curves is a separate step, and doing it robustly needs the
    segments to share endpoint coordinates exactly, which is why the
    interpolation must be done identically from both sides of a shared edge.
    """
    height, width = len(field), len(field[0])
    segments = []

    for row in range(height - 1):
        for column in range(width - 1):
            corners = [(column, row + 1), (column + 1, row + 1),
                       (column + 1, row), (column, row)]
            values = [field[row + 1][column], field[row + 1][column + 1],
                      field[row][column + 1], field[row][column]]

            code = corner_code(values, level)
            pairs = CASES[code]

            if code in (5, 10) and resolve_saddle:
                pairs = _resolve(values, code, level)

            crossings = {}
            for edge in range(4):
                start, end = corners[edge], corners[(edge + 1) % 4]
                crossings[edge] = interpolate(start, end, values[edge],
                                              values[(edge + 1) % 4], level)

            for first, second in pairs:
                segments.append((crossings[first], crossings[second]))

    return segments


def _resolve(values, code, level):
    """Pick a pairing for a saddle from the average of the four corners.

    The samples alone do not decide it: two corners are above the level and the
    two opposite ones below, and both ways of connecting them fit the data.
    Using the corner average as a stand-in for the value at the cell centre
    picks the interpretation that keeps the higher region connected, and it is
    the standard tie-break.

    Choosing inconsistently between neighbouring cells is what leaves gaps in
    an otherwise closed contour, which is the practical reason to have a rule
    at all rather than to pick arbitrarily.
    """
    centre = sum(values) / 4
    above = centre >= level

    if code == 5:
        return [(0, 1), (2, 3)] if above else [(0, 3), (1, 2)]
    return [(0, 3), (1, 2)] if above else [(0, 1), (2, 3)]


def sample(function, x_range, y_range, resolution):
    """Sample a function on a regular grid, in image row order."""
    x_min, x_max = x_range
    y_min, y_max = y_range
    field = []

    for row in range(resolution):
        y = y_min + (y_max - y_min) * row / (resolution - 1)
        field.append([function(x_min + (x_max - x_min) * column / (resolution - 1), y)
                      for column in range(resolution)])

    return field


def contour_length(segments):
    """Total length of a set of contour segments."""
    return sum(((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5 for a, b in segments)


def to_grid_coordinates(segments, x_range, y_range, resolution):
    """Map segment endpoints from grid indices back to the sampled domain."""
    x_min, x_max = x_range
    y_min, y_max = y_range
    step_x = (x_max - x_min) / (resolution - 1)
    step_y = (y_max - y_min) / (resolution - 1)

    def convert(point):
        """Map one grid index pair into the sampled domain."""
        return (x_min + point[0] * step_x, y_min + point[1] * step_y)

    return [(convert(a), convert(b)) for a, b in segments]


def is_closed(segments, tolerance=1e-9):
    """Whether the segments form closed loops, with every endpoint matched.

    A correct contour of a field with no boundary crossings is always closed,
    because the level set of a continuous function separates the plane. An
    unmatched endpoint means either the contour ran off the edge of the grid or
    the saddle cases were resolved inconsistently.
    """
    counts = {}
    for a, b in segments:
        for point in (a, b):
            key = (round(point[0] / tolerance), round(point[1] / tolerance))
            counts[key] = counts.get(key, 0) + 1

    return all(count % 2 == 0 for count in counts.values())
