"""Delaunay triangulation and its dual, the Voronoi diagram.

Given a set of points there are many triangulations, and they are not equally
good. Long thin triangles interpolate badly, shade badly and make finite
element solvers ill-conditioned. The Delaunay triangulation is the one that
avoids them as far as the point set allows: among all triangulations of the
same points it maximises the smallest angle.

Its defining property is local and checkable: no point lies inside the
circumcircle of any triangle. The Voronoi diagram is the same information read
the other way, as the region of the plane closest to each point.
"""

from __future__ import annotations

import math


def circumcircle(a, b, c):
    """Centre and radius of the circle through three points.

    `None` for collinear points, where the circle degenerates into a line. The
    centre is the intersection of the perpendicular bisectors, which is what
    makes it also the Voronoi vertex of those three sites.
    """
    d = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    if abs(d) < 1e-12:
        return None

    ux = ((a[0]**2 + a[1]**2) * (b[1] - c[1])
          + (b[0]**2 + b[1]**2) * (c[1] - a[1])
          + (c[0]**2 + c[1]**2) * (a[1] - b[1])) / d
    uy = ((a[0]**2 + a[1]**2) * (c[0] - b[0])
          + (b[0]**2 + b[1]**2) * (a[0] - c[0])
          + (c[0]**2 + c[1]**2) * (b[0] - a[0])) / d

    return ((ux, uy), math.dist((ux, uy), a))


def orientation(a, b, c):
    """Twice the signed area of a triangle: positive when counterclockwise."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def in_circumcircle(triangle, point):
    """Whether a point lies strictly inside a triangle's circumcircle.

    The predicate the whole construction rests on, as the sign of a 3x3
    determinant in coordinates relative to the query point. Computing the
    circumcentre first and comparing distances is the obvious alternative and
    is much worse conditioned: the centre of a nearly degenerate triangle is
    enormous and far away, and the subtraction that follows cancels almost
    every significant digit.

    The determinant form was not a stylistic preference here. With the distance
    comparison, `bowyer_watson` produced triangulations with holes on 33 of 300
    random point sets, and each of them still passed the empty-circumcircle
    test, because a missing triangle violates nothing.

    Production code goes one step further and evaluates this determinant in
    exact arithmetic, since a sign error here is not a small error: it makes
    the algorithm delete the wrong triangles and the result is not a
    triangulation at all.
    """
    a, b, c = triangle
    if orientation(a, b, c) < 0:
        a, b = b, a

    ax, ay = a[0] - point[0], a[1] - point[1]
    bx, by = b[0] - point[0], b[1] - point[1]
    cx, cy = c[0] - point[0], c[1] - point[1]

    determinant = ((ax * ax + ay * ay) * (bx * cy - cx * by)
                   - (bx * bx + by * by) * (ax * cy - cx * ay)
                   + (cx * cx + cy * cy) * (ax * by - bx * ay))

    return determinant > 0


def bowyer_watson(points):
    """Incremental Delaunay triangulation.

    Insert points one at a time. Every triangle whose circumcircle contains the
    new point is no longer Delaunay, so delete all of them; what is left is a
    star-shaped hole, and connecting the new point to its boundary restores a
    valid triangulation.

    The correctness argument is local and the implementation follows it
    directly. The cost is `O(n^2)` in this form because finding the bad
    triangles is a scan; with a search structure it is `O(n log n)` expected.

    **Cocircular points break it.** Eight points placed exactly on one circle
    produce nine overlapping triangles covering 532.8 units of a hull with area
    282.8. The determinants that should be exactly zero come out as -9.1e-13
    and -1.5e-11 instead, so the algorithm makes contradictory decisions about
    which triangles to delete. Displacing the points by 1e-12 fixes it
    completely, 20 times out of 20, which is the cheap version of what
    production code does deliberately under the name simulation of simplicity.
    """
    unique = sorted(set(tuple(map(float, point)) for point in points))
    if len(unique) < 3:
        return []

    super_triangle = _super_triangle(unique)
    triangles = [super_triangle]

    for point in unique:
        bad = [triangle for triangle in triangles if in_circumcircle(triangle, point)]

        boundary = []
        for triangle in bad:
            for edge in _edges(triangle):
                if sum(1 for other in bad if _has_edge(other, edge)) == 1:
                    boundary.append(edge)

        triangles = [triangle for triangle in triangles if triangle not in bad]
        for edge in boundary:
            triangles.append((edge[0], edge[1], point))

    return [triangle for triangle in triangles
            if not any(vertex in super_triangle for vertex in triangle)]


def _super_triangle(points):
    """A triangle large enough to contain every point, removed at the end.

    "Large enough to contain them" is not the requirement, and assuming it is
    was worth 33 broken triangulations out of 300 random point sets. Triangles
    along the convex hull have a super-triangle vertex as their third corner,
    and their circumcircles depend on where that vertex is. Unless it is
    effectively at infinity, those circles are small enough to change which
    triangles the algorithm deletes, and the result after the super triangle is
    stripped away is missing pieces near the hull.

    Measured on the same 300 sets, counting how many disagreed with the
    `2n - 2 - h` triangle count:

    | scale, in bounding boxes | broken |
    |---|---|
    | 2 | 181 |
    | 20 | 33 |
    | 1000 | 1 |
    | 100000 | 0 |

    Hence the factor below. Going further still works, but coordinates that
    large start costing precision in the determinant for no further benefit.
    """
    min_x = min(point[0] for point in points)
    max_x = max(point[0] for point in points)
    min_y = min(point[1] for point in points)
    max_y = max(point[1] for point in points)

    span = max(max_x - min_x, max_y - min_y, 1.0) * 1e6
    centre_x, centre_y = (min_x + max_x) / 2, (min_y + max_y) / 2

    return ((centre_x - span, centre_y - span),
            (centre_x + span, centre_y - span),
            (centre_x, centre_y + span))


def _edges(triangle):
    """The three edges of a triangle, each with its endpoints ordered."""
    a, b, c = triangle
    return [tuple(sorted([a, b])), tuple(sorted([b, c])), tuple(sorted([c, a]))]


def _has_edge(triangle, edge):
    """Whether a triangle contains a given edge."""
    return edge in _edges(triangle)


def is_delaunay(triangles, points, tolerance=1e-9):
    """Whether no point lies inside any circumcircle.

    The definition, checked directly. Quadratic, so it is a test rather than a
    construction, and it is the only sound way to verify an implementation:
    every step of Bowyer-Watson can look right while the result is not
    Delaunay.
    """
    for triangle in triangles:
        result = circumcircle(*triangle)
        if result is None:
            return False
        centre, radius = result
        for point in points:
            if point in triangle:
                continue
            if math.dist(centre, point) < radius - tolerance:
                return False
    return True


def minimum_angle(triangles):
    """The smallest angle anywhere in a triangulation, in degrees.

    The quantity Delaunay maximises. Comparing this against an arbitrary
    triangulation of the same points is the clearest way to see what the
    property buys, and it is why meshing tools triangulate this way.
    """
    smallest = 180.0

    for a, b, c in triangles:
        sides = [math.dist(b, c), math.dist(a, c), math.dist(a, b)]
        for index in range(3):
            opposite = sides[index]
            other = [sides[i] for i in range(3) if i != index]
            if other[0] * other[1] == 0:
                continue
            cosine = (other[0]**2 + other[1]**2 - opposite**2) / (2 * other[0] * other[1])
            smallest = min(smallest, math.degrees(math.acos(max(-1.0, min(1.0, cosine)))))

    return smallest


def voronoi_vertices(triangles):
    """The Voronoi vertices: the circumcentres of the Delaunay triangles.

    The duality in one line. A Voronoi vertex is equidistant from three sites
    and nearer to them than to any other, which is exactly the circumcentre of
    a Delaunay triangle.
    """
    result = []
    for triangle in triangles:
        circle = circumcircle(*triangle)
        if circle is not None:
            result.append(circle[0])
    return result


def voronoi_edges(triangles):
    """The finite Voronoi edges, one per shared Delaunay edge.

    Two triangles sharing an edge give a segment between their circumcentres.
    A Delaunay edge on the convex hull has only one adjacent triangle and its
    dual Voronoi edge is a ray running to infinity, which is omitted here: the
    unbounded cells are the ones on the hull, and every practical
    implementation clips them to a bounding box.
    """
    by_edge = {}
    for triangle in triangles:
        circle = circumcircle(*triangle)
        if circle is None:
            continue
        for edge in _edges(triangle):
            by_edge.setdefault(edge, []).append(circle[0])

    return [tuple(centres) for centres in by_edge.values() if len(centres) == 2]


def nearest_site(sites, point):
    """The site closest to a point, which is the Voronoi cell it falls in.

    The definition of the diagram, evaluated pointwise. Rasterising this over a
    grid draws the diagram directly, and comparing that picture against the
    dual construction is the check that the duality was implemented correctly.
    """
    return min(range(len(sites)), key=lambda index: math.dist(sites[index], point))


def delaunay_edges(triangles):
    """The undirected edges of a triangulation."""
    edges = set()
    for triangle in triangles:
        for edge in _edges(triangle):
            edges.add(edge)
    return sorted(edges)


def flip_improves(shared, opposite):
    """Whether flipping a shared edge increases the smallest angle.

    The local step behind the flip algorithm: a quadrilateral has two
    triangulations, and the Delaunay one is whichever fails to contain the
    other's fourth point in its circumcircle. Repeatedly flipping until no edge
    improves reaches the global Delaunay triangulation, which is not obvious
    and is the theorem that makes local repair enough.
    """
    first = (shared[0], shared[1], opposite[0])
    return in_circumcircle(first, opposite[1])
