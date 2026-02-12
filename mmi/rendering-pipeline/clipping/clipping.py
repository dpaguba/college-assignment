"""Clipping: removing what falls outside the viewing volume.

Not an optimisation. Geometry behind the camera has a negative `w`, and after
the perspective divide it reappears in front of the camera, mirrored. Without
clipping against the near plane a triangle straddling the camera renders as a
shape that does not exist anywhere in the scene.

The algorithms differ in what they clip and how they decide. Cohen-Sutherland
rejects cheaply and often, Liang-Barsky computes the answer directly, and
Sutherland-Hodgman handles polygons by clipping against one plane at a time.
"""

from __future__ import annotations

INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8


def outcode(x, y, window):
    """Four bits saying which sides of the window a point is beyond.

    The encoding is what makes the algorithm fast: both codes zero means the
    segment is fully inside, and a non-zero bitwise **and** means both
    endpoints are beyond the same edge, so the segment cannot cross the window
    at all. Two integer operations decide the common cases.
    """
    left, bottom, right, top = window
    code = INSIDE
    if x < left:
        code |= LEFT
    elif x > right:
        code |= RIGHT
    if y < bottom:
        code |= BOTTOM
    elif y > top:
        code |= TOP
    return code


def cohen_sutherland(x0, y0, x1, y1, window):
    """Clip a segment to a rectangle by repeatedly cutting at a crossed edge.

    Take an endpoint that is outside, move it to where the segment meets the
    edge it is beyond, and try the cheap tests again. Each iteration removes at
    least one outcode bit, so it terminates after at most four cuts.
    """
    left, bottom, right, top = window
    code0, code1 = outcode(x0, y0, window), outcode(x1, y1, window)

    while True:
        if not (code0 | code1):
            return (x0, y0, x1, y1)
        if code0 & code1:
            return None

        code = code0 or code1
        if code & TOP:
            x = x0 + (x1 - x0) * (top - y0) / (y1 - y0)
            y = top
        elif code & BOTTOM:
            x = x0 + (x1 - x0) * (bottom - y0) / (y1 - y0)
            y = bottom
        elif code & RIGHT:
            y = y0 + (y1 - y0) * (right - x0) / (x1 - x0)
            x = right
        else:
            y = y0 + (y1 - y0) * (left - x0) / (x1 - x0)
            x = left

        if code == code0:
            x0, y0 = x, y
            code0 = outcode(x0, y0, window)
        else:
            x1, y1 = x, y
            code1 = outcode(x1, y1, window)


def liang_barsky(x0, y0, x1, y1, window):
    """Clip a segment by narrowing the parameter interval, one edge at a time.

    Write the segment as `p + t d` for `t` in `[0, 1]`. Each edge gives an
    inequality `t p_k <= q_k`; a negative `p_k` means the segment enters there
    and raises the lower bound, a positive one means it leaves and lowers the
    upper bound. When the bounds cross, the segment misses the window.

    No iteration and no repeated intersection computation, and the parameter
    values come out directly, which is what an interpolating rasteriser wants
    for the attributes at the clipped endpoints.
    """
    left, bottom, right, top = window
    dx, dy = x1 - x0, y1 - y0
    enter, leave = 0.0, 1.0

    for p, q in ((-dx, x0 - left), (dx, right - x0), (-dy, y0 - bottom), (dy, top - y0)):
        if p == 0:
            if q < 0:
                return None
            continue
        ratio = q / p
        if p < 0:
            if ratio > leave:
                return None
            enter = max(enter, ratio)
        else:
            if ratio < enter:
                return None
            leave = min(leave, ratio)

    return (x0 + enter * dx, y0 + enter * dy, x0 + leave * dx, y0 + leave * dy)


def sutherland_hodgman(polygon, window):
    """Clip a polygon against a convex window, one edge of the window at a time.

    Feed the polygon through four passes, each keeping the part on the inside
    of one edge. Every pass emits, for each input edge, the crossing point if
    it changes side and the endpoint if it ends inside.

    The output is always a single closed polygon, which is convenient and also
    the algorithm's known flaw: clipping a concave polygon that leaves and
    re-enters the window produces two pieces joined by a degenerate edge along
    the boundary. Convex input never triggers it.
    """
    left, bottom, right, top = window
    edges = (("left", left), ("right", right), ("bottom", bottom), ("top", top))
    output = list(polygon)

    for name, boundary in edges:
        if not output:
            return []
        current, output = output, []

        for index in range(len(current)):
            start, end = current[index - 1], current[index]
            start_in, end_in = _inside(start, name, boundary), _inside(end, name, boundary)

            if end_in:
                if not start_in:
                    output.append(_intersect(start, end, name, boundary))
                output.append(end)
            elif start_in:
                output.append(_intersect(start, end, name, boundary))

    return output


def _inside(point, name, boundary):
    """Whether a point is on the keeping side of one window edge."""
    if name == "left":
        return point[0] >= boundary
    if name == "right":
        return point[0] <= boundary
    if name == "bottom":
        return point[1] >= boundary
    return point[1] <= boundary


def _intersect(start, end, name, boundary):
    """Where a segment crosses one window edge."""
    if name in ("left", "right"):
        ratio = (boundary - start[0]) / (end[0] - start[0])
        return (boundary, start[1] + ratio * (end[1] - start[1]))
    ratio = (boundary - start[1]) / (end[1] - start[1])
    return (start[0] + ratio * (end[0] - start[0]), boundary)


def clip_near_plane(triangle, near):
    """Clip a triangle against the near plane in camera space.

    The one clip that cannot be skipped. Vertices with `z > -near` are behind
    the plane; cutting them off can leave a quadrilateral, which is then
    retriangulated. This is why a renderer can be handed triangles and emit
    more triangles than it received.
    """
    inside = [vertex for vertex in triangle if vertex[2] <= -near]
    outside = [vertex for vertex in triangle if vertex[2] > -near]

    if len(inside) == 3:
        return [tuple(triangle)]
    if not inside:
        return []

    def cut(a, b):
        """Where the edge from `a` to `b` crosses the near plane."""
        ratio = (-near - a[2]) / (b[2] - a[2])
        return tuple(a[axis] + ratio * (b[axis] - a[axis]) for axis in range(3))

    if len(inside) == 1:
        a = inside[0]
        return [(a, cut(a, outside[0]), cut(a, outside[1]))]

    a, b = inside
    c = outside[0]
    first, second = cut(a, c), cut(b, c)
    return [(a, b, second), (a, second, first)]


def back_facing(a, b, c):
    """Whether a screen-space triangle faces away, by the sign of its area.

    Counterclockwise is the front by convention. A closed opaque mesh has half
    its triangles pointing away from the camera at any moment, and none of them
    can be visible, so discarding them by one sign test halves the work before
    any pixel is touched.
    """
    return (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1]) < 0
