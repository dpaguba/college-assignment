# Polyline simplification

Douglas-Peucker keeps the point furthest from the line between the ends when
that distance exceeds the tolerance, then recurses on both halves. It is fast
and it respects the tolerance: over 180 random cases the resulting error
never exceeded the tolerance given.

At tolerance zero it keeps everything except the points that lie exactly on a
segment, which is correct: removing a collinear point does not change the
curve.

## It is not the minimum

The min-# version of Imai and Iri builds the graph of all admissible
shortcuts and takes the shortest path through it, which is the fewest points
that stay within the tolerance. On 180 random polylines the exact method used
strictly fewer points than Douglas-Peucker in 35 of them, about one in five.

On the line in `greedy_is_not_optimal`, Douglas-Peucker keeps 5 points and
the optimum needs 4. The difference comes from the first split: the recursive
method commits to the furthest point and never reconsiders, while the path
search weighs every shortcut against every other.
