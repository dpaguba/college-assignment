"""Closest pair of points: the two nearest points among n, in O(n log n)."""

from __future__ import annotations

from math import dist, inf

def closest_pair(points):
    """Return the smallest distance between any two points, and the pair.

    Checking every pair costs O(n²). Divide and conquer gets it to O(n log n),
    and the interesting part is not the split but what happens at the seam.

    Sort by x, split at the median, and solve both halves. Let d be the better
    of the two answers. A closer pair must then have one point in each half and
    both within d of the dividing line, so only that strip needs checking.

    The strip can still hold every point, so scanning it naively brings the n²
    back. The saving comes from a geometric fact: **within the strip, sorted by
    y, a point can only be closer than d to the next seven.** Any more and two
    points on the same side would be closer than d to each other, which
    contradicts d being the best within a half.

    That constant, seven, is what makes the merge step linear and the whole
    algorithm n log n. It is the clearest example in the course of a bound that
    comes from geometry rather than from bookkeeping.

    Seven neighbours in the strip is enough: an eighth would force two points
    on one side of the dividing line to be closer to each other than the best
    distance already found there. Points are tracked by identity, so two
    identical coordinates still count as a pair at distance zero.
    """
    if len(points) < 2:
        raise ValueError("a closest pair needs at least two points")

    by_x = sorted(points)
    by_y = sorted(points, key=lambda point: point[1])

    def solve(xs, ys):
        """The closest pair in the range, and its distance."""
        if len(xs) <= 3:
            best = (inf, None)
            for index, left in enumerate(xs):
                for right in xs[index + 1 :]:
                    separation = dist(left, right)
                    if separation < best[0]:
                        best = (separation, (left, right))
            return best

        middle = len(xs) // 2
        divider = xs[middle][0]
        left_xs, right_xs = xs[:middle], xs[middle:]
        left_set = set(map(id, left_xs))

        left_ys = [point for point in ys if id(point) in left_set]
        right_ys = [point for point in ys if id(point) not in left_set]

        best = min(solve(left_xs, left_ys), solve(right_xs, right_ys), key=lambda item: item[0])
        limit = best[0]

        strip = [point for point in ys if abs(point[0] - divider) < limit]
        for index, point in enumerate(strip):
            for other in strip[index + 1 : index + 8]:
                separation = dist(point, other)
                if separation < best[0]:
                    best = (separation, (point, other))

        return best

    return solve(by_x, by_y)
