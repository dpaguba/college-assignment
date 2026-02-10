"""Collision detection: deciding what is touching what.

The naive answer, test every pair exactly, costs `O(n^2)` exact tests and is
too slow twice over. Every real system therefore splits the problem in two: a
broad phase that cheaply rejects most pairs, and a narrow phase that answers
exactly for the few that survive.

The same split appears in ray tracing, where a bounding volume hierarchy is the
broad phase and the triangle intersection is the narrow one. The trade is
identical: a conservative test that is allowed false positives but never false
negatives, followed by an exact one.
"""

from __future__ import annotations

import math


def bounding_box(points):
    """The axis-aligned box containing a point set."""
    return ((min(point[0] for point in points), min(point[1] for point in points)),
            (max(point[0] for point in points), max(point[1] for point in points)))


def aabb_overlap(low_a, high_a, low_b, high_b):
    """Whether two axis-aligned boxes overlap, by the separating interval rule.

    Two boxes are disjoint exactly when they are disjoint on some axis, so four
    comparisons decide it. Touching counts as overlapping, which is the right
    convention for a broad phase: it may return extra pairs but must never miss
    one.
    """
    return not (high_a[0] < low_b[0] or high_b[0] < low_a[0]
                or high_a[1] < low_b[1] or high_b[1] < low_a[1])


def sphere_overlap(centre_a, radius_a, centre_b, radius_b):
    """Whether two circles overlap, comparing squared distances.

    Cheaper than a box test and rotation invariant, which is why a bounding
    sphere is preferred for objects that turn: the box has to be rebuilt every
    frame and the sphere does not.
    """
    dx, dy = centre_a[0] - centre_b[0], centre_a[1] - centre_b[1]
    reach = radius_a + radius_b
    return dx * dx + dy * dy <= reach * reach


def sat_overlap(first, second):
    """Separating axis test for two convex polygons.

    Two convex shapes are disjoint exactly when some line separates them, and
    if one exists then one parallel to an edge of either shape exists. So
    projecting both shapes onto each edge normal and looking for a gap decides
    it exactly, in a number of tests equal to the number of edges.

    Convexity is essential and not a technicality. For concave shapes the
    theorem is false, and the usual answer is to decompose them into convex
    pieces first.
    """
    for polygon in (first, second):
        for index in range(len(polygon)):
            a, b = polygon[index], polygon[(index + 1) % len(polygon)]
            axis = (-(b[1] - a[1]), b[0] - a[0])

            min_a, max_a = _project(first, axis)
            min_b, max_b = _project(second, axis)

            if max_a < min_b or max_b < min_a:
                return False

    return True


def _project(polygon, axis):
    """Interval covered by a polygon projected onto an axis."""
    values = [point[0] * axis[0] + point[1] * axis[1] for point in polygon]
    return min(values), max(values)


def penetration(first, second):
    """How deep two polygons overlap and along which direction, in one pass.

    The axis of least overlap is the shortest way out, so pushing one shape
    along it by that distance separates them. This is what a physics engine
    needs: knowing that two things collided is not enough, the response needs a
    direction and a magnitude.
    """
    best_depth = math.inf
    best_axis = (0.0, 0.0)

    for polygon in (first, second):
        for index in range(len(polygon)):
            a, b = polygon[index], polygon[(index + 1) % len(polygon)]
            axis = (-(b[1] - a[1]), b[0] - a[0])
            length = math.hypot(*axis)
            if length < 1e-12:
                continue
            axis = (axis[0] / length, axis[1] / length)

            min_a, max_a = _project(first, axis)
            min_b, max_b = _project(second, axis)

            if max_a < min_b or max_b < min_a:
                return 0.0, (0.0, 0.0)

            overlap = min(max_a, max_b) - max(min_a, min_b)
            if overlap < best_depth:
                best_depth = overlap
                centre_a = sum(point[0] * axis[0] + point[1] * axis[1]
                               for point in first) / len(first)
                centre_b = sum(point[0] * axis[0] + point[1] * axis[1]
                               for point in second) / len(second)
                best_axis = axis if centre_b > centre_a else (-axis[0], -axis[1])

    return best_depth, best_axis


def brute_force_pairs(boxes):
    """Every overlapping pair, tested exhaustively.

    The specification the broad phase is checked against, and the reason a
    broad phase exists: 300 objects means 44850 pair tests per frame before
    anything is drawn.
    """
    pairs = set()
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if aabb_overlap(boxes[i][0], boxes[i][1], boxes[j][0], boxes[j][1]):
                pairs.add((i, j))
    return pairs


def spatial_hash_pairs(boxes, cell=1.0):
    """Overlapping pairs found through a uniform grid.

    Each object is registered in every cell its box touches, and only objects
    sharing a cell are tested. Objects far apart never meet, so the cost drops
    from quadratic to roughly linear in the number of objects for scenes where
    objects are small relative to the world.

    The cell size is the whole tuning problem. Too small and large objects are
    registered in many cells; too large and every object shares a cell with
    every other, which is brute force with extra bookkeeping.
    """
    grid = {}

    for index, (low, high) in enumerate(boxes):
        for key in _cells(low, high, cell):
            grid.setdefault(key, []).append(index)

    pairs = set()
    for occupants in grid.values():
        for i in range(len(occupants)):
            for j in range(i + 1, len(occupants)):
                a, b = sorted((occupants[i], occupants[j]))
                if (a, b) in pairs:
                    continue
                if aabb_overlap(boxes[a][0], boxes[a][1], boxes[b][0], boxes[b][1]):
                    pairs.add((a, b))

    return pairs


def spatial_hash_checks(boxes, cell=1.0):
    """How many pair tests the grid actually performed.

    The number that says whether the broad phase is earning its keep. Compared
    against `n(n-1)/2`, it is the speedup, and it depends entirely on the cell
    size being matched to the object size.
    """
    grid = {}
    for index, (low, high) in enumerate(boxes):
        for key in _cells(low, high, cell):
            grid.setdefault(key, []).append(index)

    seen = set()
    for occupants in grid.values():
        for i in range(len(occupants)):
            for j in range(i + 1, len(occupants)):
                seen.add(tuple(sorted((occupants[i], occupants[j]))))

    return len(seen)


def _cells(low, high, size):
    """Grid cells touched by a box."""
    for x in range(int(math.floor(low[0] / size)), int(math.floor(high[0] / size)) + 1):
        for y in range(int(math.floor(low[1] / size)), int(math.floor(high[1] / size)) + 1):
            yield (x, y)


def swept_sphere(start, end, target, radius, target_radius):
    """When along a movement two circles first touch, or `None`.

    Testing only the start and end positions misses anything moving faster than
    its own size in one frame, which is called tunnelling: the bullet is on one
    side of the wall in one frame and past it in the next, and no discrete test
    ever sees it inside.

    Solving for the time is a quadratic in the movement parameter, the same
    algebra as a ray against a sphere, with the two radii added.
    """
    dx, dy = end[0] - start[0], end[1] - start[1]
    fx, fy = start[0] - target[0], start[1] - target[1]
    reach = radius + target_radius

    a = dx * dx + dy * dy
    b = 2 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - reach * reach

    if a < 1e-15:
        return 0.0 if c <= 0 else None

    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return None

    root = math.sqrt(discriminant)
    for time in ((-b - root) / (2 * a), (-b + root) / (2 * a)):
        if 0.0 <= time <= 1.0:
            return time

    return None


def _convex_hull(points):
    """Convex hull by monotone chain, so the tests have convex input."""
    ordered = sorted(set(tuple(point) for point in points))
    if len(ordered) < 3:
        return ordered

    def build(sequence):
        """One half of the hull, popping points that turn the wrong way."""
        chain = []
        for point in sequence:
            while len(chain) >= 2:
                a, b = chain[-2], chain[-1]
                if ((b[0] - a[0]) * (point[1] - a[1])
                        - (b[1] - a[1]) * (point[0] - a[0])) <= 0:
                    chain.pop()
                else:
                    break
            chain.append(point)
        return chain

    return build(ordered)[:-1] + build(ordered[::-1])[:-1]


def _sampled_overlap(first, second, resolution):
    """Whether two polygons share area, by sampling, as an independent oracle.

    Deliberately not the separating axis test: checking an implementation
    against itself proves nothing. Returns `None` when the answer is too close
    to call at this resolution, so that a near miss is not counted as a
    disagreement.
    """
    low_a, high_a = bounding_box(first)
    low_b, high_b = bounding_box(second)

    low = (max(low_a[0], low_b[0]), max(low_a[1], low_b[1]))
    high = (min(high_a[0], high_b[0]), min(high_a[1], high_b[1]))

    if low[0] > high[0] or low[1] > high[1]:
        return False

    margin = 0.0
    hit = False
    for i in range(resolution):
        for j in range(resolution):
            point = (low[0] + (high[0] - low[0]) * (i + 0.5) / resolution,
                     low[1] + (high[1] - low[1]) * (j + 0.5) / resolution)
            if _inside(first, point) and _inside(second, point):
                hit = True
                break
        if hit:
            break

    if hit:
        return True

    margin = min(_clearance(first, second), _clearance(second, first))
    step = max((high[0] - low[0]), (high[1] - low[1])) / resolution
    return None if margin < 2 * step else False


def _inside(polygon, point):
    """Whether a point is inside a counterclockwise convex polygon."""
    for index in range(len(polygon)):
        a, b = polygon[index], polygon[(index + 1) % len(polygon)]
        if (b[0] - a[0]) * (point[1] - a[1]) - (b[1] - a[1]) * (point[0] - a[0]) < 0:
            return False
    return True


def _clearance(first, second):
    """Smallest distance from the vertices of one polygon to the other."""
    best = math.inf
    for point in second:
        for index in range(len(first)):
            a, b = first[index], first[(index + 1) % len(first)]
            best = min(best, _point_to_segment(point, a, b))
    return best


def _point_to_segment(point, start, end):
    """Distance from a point to a segment."""
    dx, dy = end[0] - start[0], end[1] - start[1]
    if dx == 0.0 and dy == 0.0:
        return math.dist(point, start)
    ratio = ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / (dx * dx + dy * dy)
    ratio = max(0.0, min(1.0, ratio))
    return math.dist(point, (start[0] + ratio * dx, start[1] + ratio * dy))
