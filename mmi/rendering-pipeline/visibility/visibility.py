"""Hidden surface removal: deciding what is in front of what.

Three answers, and they differ in where the sorting happens. The painter's
algorithm sorts the polygons, the z-buffer sorts per pixel, and a BSP tree
sorts once at build time and then reads the order off the tree for any
viewpoint.

Everything else being equal, the per-pixel answer wins, because the problem is
per pixel: two triangles can each be in front of the other depending on where
you look, and no ordering of the triangles themselves can express that.
"""

from __future__ import annotations

import math


class DepthBuffer:
    """A z-buffer: one depth per pixel, keep whichever fragment is nearer.

    The idea is almost embarrassingly simple and it is why it won. There is no
    sorting, no preprocessing and no restriction on the geometry, the cost is
    one comparison and one memory write per fragment, and triangles can arrive
    in any order at all.

    The price is memory, which is why it took until the nineties to become
    standard, and that transparency does not work: a fragment behind a
    transparent one is discarded before anything can blend it.
    """

    def __init__(self, width, height):
        """Allocate a buffer with every pixel at infinite depth."""
        self.width, self.height = width, height
        self.depth = [[math.inf] * width for _ in range(height)]
        self.colour = [[None] * width for _ in range(height)]
        self.tests = 0
        self.writes = 0

    def write(self, x, y, z, value):
        """Keep a fragment if it is nearer than what is already there."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        self.tests += 1
        if z < self.depth[y][x]:
            self.depth[y][x] = z
            self.colour[y][x] = value
            self.writes += 1
            return True
        return False

    def overdraw(self):
        """Writes per test: how much work the order of the triangles wasted.

        Drawing front to back makes the depth test reject early and this ratio
        drops. Drawing back to front makes every fragment win and then be
        overwritten, which is the worst case and the whole reason engines
        bother to sort roughly before submitting.
        """
        return self.writes / max(1, self.tests)


def painter_order(polygons, camera):
    """Sort polygons back to front by the distance of their centroid.

    Then draw them in that order and let later ones cover earlier ones. No
    depth buffer needed, which mattered when memory was expensive.

    Sorting by centroid is the cheap approximation, and it is wrong whenever
    two polygons overlap in depth. `has_cycle` finds the cases it cannot fix at
    all.
    """
    def distance(polygon):
        """Negated squared distance from the camera to a polygon's centroid."""
        centroid = tuple(sum(vertex[axis] for vertex in polygon) / len(polygon)
                         for axis in range(3))
        return -sum((a - b) ** 2 for a, b in zip(centroid, camera))

    return sorted(range(len(polygons)), key=lambda index: distance(polygons[index]))


def occludes(first, second, camera):
    """Whether `first` is unambiguously in front of `second` from the camera.

    A partial order at best: three long triangles can be arranged so that each
    occludes the next in a cycle, and then no drawing order is correct. The
    only fix is to split one of them, which is what a BSP tree does in advance.
    """
    return (min(_ray_depth(vertex, camera) for vertex in first)
            < min(_ray_depth(vertex, camera) for vertex in second))


def _ray_depth(point, camera):
    """Distance from the camera to a point."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(point, camera)))


def has_cycle(polygons, camera):
    """Whether the occlusion relation contains a cycle, by depth overlap.

    Two polygons whose depth ranges overlap cannot be ordered by depth alone.
    Three of them mutually overlapping is the classic configuration where the
    painter's algorithm has no correct answer, and it is not a rare corner
    case: any two interpenetrating surfaces produce it.
    """
    ranges = []
    for polygon in polygons:
        depths = [_ray_depth(vertex, camera) for vertex in polygon]
        ranges.append((min(depths), max(depths)))

    for i in range(len(ranges)):
        for j in range(i + 1, len(ranges)):
            if ranges[i][0] < ranges[j][1] and ranges[j][0] < ranges[i][1]:
                return True
    return False


class BSPNode:
    """A node of a binary space partitioning tree.

    Each node holds a splitting plane and the polygons lying on it, with
    everything in front in one subtree and everything behind in the other.
    """

    def __init__(self, plane, coplanar):
        """Create a node holding a splitting plane and the polygons on it."""
        self.plane = plane
        self.coplanar = coplanar
        self.front = None
        self.back = None


def plane_of(polygon):
    """The plane through a polygon, as a normal and an offset, by Newell's method.

    Taking the cross product of the first two edges is the obvious way and it
    breaks on exactly the polygons a BSP tree produces: a split inserts a
    vertex on an existing edge, so the first three vertices are often
    collinear and the cross product is zero. Newell's method sums a term over
    every edge, so it only degenerates if the whole polygon does, and it also
    gives a sensible answer for vertices that are not quite planar.
    """
    normal = [0.0, 0.0, 0.0]
    for index in range(len(polygon)):
        current, following = polygon[index], polygon[(index + 1) % len(polygon)]
        normal[0] += (current[1] - following[1]) * (current[2] + following[2])
        normal[1] += (current[2] - following[2]) * (current[0] + following[0])
        normal[2] += (current[0] - following[0]) * (current[1] + following[1])

    length = math.sqrt(sum(component ** 2 for component in normal))
    if length < 1e-12:
        raise ValueError("degenerate polygon has no plane")

    normal = tuple(component / length for component in normal)
    centroid = tuple(sum(vertex[axis] for vertex in polygon) / len(polygon)
                     for axis in range(3))
    return normal, sum(n * c for n, c in zip(normal, centroid))


def classify(polygon, plane, epsilon=1e-9):
    """Which side of a plane a polygon lies on, or whether it straddles it."""
    normal, offset = plane
    signs = set()
    for vertex in polygon:
        distance = sum(n * v for n, v in zip(normal, vertex)) - offset
        if distance > epsilon:
            signs.add(1)
        elif distance < -epsilon:
            signs.add(-1)
    if signs == {1}:
        return "front"
    if signs == {-1}:
        return "back"
    if not signs:
        return "coplanar"
    return "spanning"


def build_bsp(polygons, split=None):
    """Build a BSP tree, splitting the polygons that straddle a plane.

    The sorting happens once, at build time, and is then valid for every
    viewpoint. That is the trade: a static scene pays a preprocessing cost and
    a growth in polygon count, and gets an exact back-to-front order in linear
    time for any camera, which is what Doom did.

    The splitting function is a parameter because choosing a good splitting
    plane is the entire engineering problem: a bad choice makes the tree
    quadratic in the number of splits it causes.
    """
    if not polygons:
        return None

    plane = plane_of(polygons[0])
    coplanar, front, back = [], [], []

    for polygon in polygons:
        side = classify(polygon, plane)
        if side == "coplanar":
            coplanar.append(polygon)
        elif side == "front":
            front.append(polygon)
        elif side == "back":
            back.append(polygon)
        elif split is not None:
            front_part, back_part = split(polygon, plane)
            if front_part:
                front.append(front_part)
            if back_part:
                back.append(back_part)
        else:
            coplanar.append(polygon)

    node = BSPNode(plane, coplanar)
    node.front = build_bsp(front, split)
    node.back = build_bsp(back, split)
    return node


def traverse_bsp(node, camera):
    """Read the back-to-front order for one camera off the tree.

    Stand at the camera, ask which side of the node's plane it is on, and
    render the far subtree, then the node, then the near subtree. Correct by
    construction: nothing in the far subtree can occlude anything in the near
    one, because the plane separates them.
    """
    if node is None:
        return []

    normal, offset = node.plane
    side = sum(n * c for n, c in zip(normal, camera)) - offset

    if side > 0:
        return (traverse_bsp(node.back, camera) + node.coplanar
                + traverse_bsp(node.front, camera))
    return (traverse_bsp(node.front, camera) + node.coplanar
            + traverse_bsp(node.back, camera))


def split_polygon(polygon, plane, epsilon=1e-9):
    """Cut a polygon along a plane into its front and back parts.

    The same walk as the Sutherland-Hodgman clipper, except both halves are
    kept instead of one. This is what makes a BSP tree exact and what makes it
    grow: every split turns one polygon into two.
    """
    normal, offset = plane
    front, back = [], []

    for index in range(len(polygon)):
        start, end = polygon[index - 1], polygon[index]
        start_distance = sum(n * v for n, v in zip(normal, start)) - offset
        end_distance = sum(n * v for n, v in zip(normal, end)) - offset

        if start_distance * end_distance < -epsilon * epsilon:
            ratio = start_distance / (start_distance - end_distance)
            crossing = tuple(start[axis] + ratio * (end[axis] - start[axis])
                             for axis in range(3))
            front.append(crossing)
            back.append(crossing)

        if end_distance >= -epsilon:
            front.append(end)
        if end_distance <= epsilon:
            back.append(end)

    return (front if len(front) >= 3 else None, back if len(back) >= 3 else None)
