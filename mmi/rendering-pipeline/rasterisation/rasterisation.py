"""Rasterisation: turning geometry into pixels.

Everything upstream works with real numbers, everything downstream works with a
grid. This is where the two meet, and every algorithm here is really an answer
to the same question: which pixel centres does this shape cover, and what value
does each of them get.

The recurring theme is integer arithmetic. Bresenham, the edge function and the
scanline fill are all built so that the inner loop uses additions on integers,
because the decision is a sign test and the sign of an integer is exact.
"""

from __future__ import annotations


def bresenham(x0, y0, x1, y1):
    """Draw a line with integer arithmetic only, no division, no rounding.

    The idea is to track the error between the ideal line and the pixel chosen
    so far. Instead of computing `y = m x + b` and rounding, the algorithm
    keeps a running error term and asks only whether it has grown past a half
    step, which is a comparison of integers.

    This form handles all eight octants by swapping the roles of the axes and
    the direction of the steps, so there is one loop rather than eight cases.
    """
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    error = dx - dy
    points = []

    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        doubled = 2 * error
        if doubled > -dy:
            error -= dy
            x0 += sx
        if doubled < dx:
            error += dx
            y0 += sy

    return points


def dda(x0, y0, x1, y1):
    """Draw a line with floating point stepping, the naive alternative.

    Correct and much easier to write, but it needs a division to get the slope,
    a floating point addition per pixel and a rounding per pixel. Bresenham
    exists because on the hardware where this mattered all three were
    expensive, and the results are the same for most lines.
    """
    steps = max(abs(x1 - x0), abs(y1 - y0))
    if steps == 0:
        return [(int(round(x0)), int(round(y0)))]

    step_x, step_y = (x1 - x0) / steps, (y1 - y0) / steps
    return [(int(round(x0 + step_x * index)), int(round(y0 + step_y * index)))
            for index in range(int(steps) + 1)]


def edge(a, b, point):
    """Signed area of the triangle `a, b, point`, doubled.

    Positive on one side of the directed line `a -> b`, negative on the other,
    zero on it. Three of these decide whether a point is inside a triangle, and
    their values double as the barycentric coordinates, which is why triangle
    rasterisers compute nothing else.
    """
    return (b[0] - a[0]) * (point[1] - a[1]) - (b[1] - a[1]) * (point[0] - a[0])


def is_top_left(a, b):
    """Whether the directed edge `a -> b` is a top or a left edge.

    Screen y grows downwards, so a top edge is horizontal and goes right, and a
    left edge goes down. The rule is arbitrary in itself; what matters is that
    it is a consistent choice which makes every shared edge belong to exactly
    one of the two triangles that meet there.
    """
    if b[1] == a[1]:
        return b[0] > a[0]
    return b[1] > a[1]


def rasterise_triangle(a, b, c, top_left=True):
    """Fill a triangle by testing every pixel in its bounding box.

    The three edge functions are affine in x and y, so their values can be
    stepped by additions across a scanline rather than recomputed. That, plus
    the fact that the test for each pixel is independent, is why this is the
    form that maps on to parallel hardware and the scanline fill is not.

    The weights come back in the order of the vertices as passed in, which
    matters because the triangle is reordered internally when it turns out to
    be clockwise. Returning them in the internal order instead makes every
    interpolated attribute of every clockwise triangle silently wrong, and
    since half the triangles of a mesh are clockwise on screen, the result
    looks like noise rather than like a bug.

    With `top_left` the fill rule breaks ties on the boundary: a pixel centre
    lying exactly on an edge belongs to the triangle only if that edge is a top
    or a left one. Without it, two triangles sharing an edge both claim the
    pixels along it, which double-blends every seam of every mesh and shows up
    as a bright line wherever transparency is involved.
    """
    area = edge(a, b, c)
    if area == 0:
        return []

    swapped = area < 0
    if swapped:
        a, b = b, a
        area = -area

    bias = [0.0 if not top_left or is_top_left(*pair) else -1e-9
            for pair in ((b, c), (c, a), (a, b))]

    min_x = int(min(a[0], b[0], c[0]))
    max_x = int(max(a[0], b[0], c[0])) + 1
    min_y = int(min(a[1], b[1], c[1]))
    max_y = int(max(a[1], b[1], c[1])) + 1

    covered = []
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            point = (x + 0.5, y + 0.5)
            w0, w1, w2 = edge(b, c, point), edge(c, a, point), edge(a, b, point)
            if (w0 + bias[0] >= 0) and (w1 + bias[1] >= 0) and (w2 + bias[2] >= 0):
                weights = (w0 / area, w1 / area, w2 / area)
                if swapped:
                    weights = (weights[1], weights[0], weights[2])
                covered.append((x, y, weights))

    return covered


def barycentric(a, b, c, point):
    """Barycentric coordinates of a point with respect to a triangle.

    The three weights sum to 1 and are all non-negative exactly inside the
    triangle. Any per-vertex quantity, colour, normal, texture coordinate,
    interpolates by weighting it with these.
    """
    area = edge(a, b, c)
    return (edge(b, c, point) / area, edge(c, a, point) / area, edge(a, b, point) / area)


def interpolate(weights, values):
    """Linear interpolation of a per-vertex value across a triangle."""
    return sum(weight * value for weight, value in zip(weights, values))


def perspective_correct(weights, values, w_values):
    """Interpolate correctly under perspective, by interpolating in `1/w`.

    Linear interpolation in screen space is wrong for anything perspective
    projected, because the projection is not affine: equal steps across the
    screen are not equal steps across the surface. Dividing each value by its
    `w`, interpolating, and dividing by the interpolated `1/w` undoes exactly
    that distortion.

    On a floor stretching into the distance the difference is unmistakable: the
    naive version makes texture rows evenly spaced on screen instead of
    bunching up towards the horizon.
    """
    inverse = [1 / w for w in w_values]
    numerator = sum(weight * value * reciprocal
                    for weight, value, reciprocal in zip(weights, values, inverse))
    denominator = sum(weight * reciprocal for weight, reciprocal in zip(weights, inverse))
    return numerator / denominator


def scanline_fill(polygon):
    """Fill an arbitrary polygon by intersecting it with horizontal lines.

    For each scanline, find where the edges cross it, sort the crossings and
    fill between them in pairs. The parity rule falls out: a point is inside
    when an odd number of crossings lie to its left.

    Horizontal edges are skipped, and each edge counts for the range
    `[y_min, y_max)`, half open. Both rules exist to stop a vertex shared by
    two edges from being counted twice, which would break the parity and leave
    a horizontal streak of unfilled pixels.
    """
    if len(polygon) < 3:
        return []

    min_y = int(min(point[1] for point in polygon))
    max_y = int(max(point[1] for point in polygon))
    filled = []

    for y in range(min_y, max_y + 1):
        sample = y + 0.5
        crossings = []

        for index in range(len(polygon)):
            start, end = polygon[index], polygon[(index + 1) % len(polygon)]
            if start[1] == end[1]:
                continue
            low, high = (start, end) if start[1] < end[1] else (end, start)
            if low[1] <= sample < high[1]:
                ratio = (sample - low[1]) / (high[1] - low[1])
                crossings.append(low[0] + ratio * (high[0] - low[0]))

        crossings.sort()
        for index in range(0, len(crossings) - 1, 2):
            left, right = crossings[index], crossings[index + 1]
            for x in range(int(left + 0.5), int(right + 0.5)):
                filled.append((x, y))

    return filled


def point_in_polygon(polygon, point):
    """Parity test for a single point, the scanline rule applied once."""
    x, y = point
    inside = False

    for index in range(len(polygon)):
        start, end = polygon[index], polygon[(index + 1) % len(polygon)]
        if (start[1] > y) != (end[1] > y):
            crossing = start[0] + (y - start[1]) / (end[1] - start[1]) * (end[0] - start[0])
            if x < crossing:
                inside = not inside

    return inside


def coverage(a, b, c, x, y, samples=4):
    """Fraction of a pixel covered by a triangle, by regular supersampling.

    This is what anti-aliasing needs: not a yes or no per pixel but a coverage
    value to blend with. Sampling on an `n x n` grid gives `n^2 + 1` possible
    values, so 4x4 supersampling can represent 17 levels of edge, which is
    enough that the staircase stops being visible.
    """
    inside = 0
    for row in range(samples):
        for column in range(samples):
            point = (x + (column + 0.5) / samples, y + (row + 0.5) / samples)
            w0, w1, w2 = edge(b, c, point), edge(c, a, point), edge(a, b, point)
            if (w0 >= 0 and w1 >= 0 and w2 >= 0) or (w0 <= 0 and w1 <= 0 and w2 <= 0):
                inside += 1
    return inside / (samples * samples)
