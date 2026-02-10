# Collision detection

Testing every pair exactly costs `O(n^2)` exact tests, and that is too slow
twice over. Every real system splits the work: a cheap broad phase that rejects
most pairs, and an exact narrow phase for the few that survive. The broad phase
may return false positives and must never return a false negative.

## Broad phase: a uniform grid

Each object is registered in every cell its box touches, and only objects
sharing a cell are tested.

| objects | brute force | grid | time, brute vs grid | same pairs |
|---|---|---|---|---|
| 100 | 4950 tests | 3 | 1.0 ms vs 0.1 ms | yes |
| 300 | 44850 tests | 39 | 8.8 ms vs 0.4 ms | yes |
| 1000 | 499500 tests | 481 | 89.1 ms vs 1.4 ms | yes |

The cell size is the entire tuning problem. For 300 objects of size 2 on a
400 x 400 field:

| cell | pair tests |
|---|---|
| 1.0 | 9 |
| 4.0 | 15 |
| 16.0 | 107 |
| 64.0 | 1305 |
| 400.0 | 44850 |

At a cell size covering the whole world the grid degenerates into brute force
with extra bookkeeping. Every setting returns the correct pairs; only the cost
changes.

## Narrow phase: the separating axis theorem

Two convex shapes are disjoint exactly when some line separates them, and if
one exists then one parallel to an edge of either shape exists. Projecting both
onto each edge normal and looking for a gap therefore decides it exactly.

Against an independent sampling oracle on 300 random convex polygon pairs:
**0** disagreements.

It is worth the cost over the bounding boxes: on 3000 random pairs, the boxes
overlapped but the shapes did not in **478 cases, 15.9%**. Two diamonds
diagonally offset are the smallest example, where the boxes overlap and the
shapes are cleanly apart.

`penetration` returns the axis of least overlap and its depth, which is the
shortest way out. Moving one shape along it by that distance separates them,
which is what a physics response needs: knowing that two things collided is not
enough.

Convexity is not a technicality. The theorem is false for concave shapes, and
the standard answer is convex decomposition first.

## Tunnelling

A sphere of radius 0.5 moving from x = 0 to x = 100 past an obstacle at x = 10:
the discrete test says no collision at the start and no collision at the end.
The swept test reports the impact at `t = 0.090000`, that is at x = 9.000.

This is why fast objects need continuous detection. Solving for the time is a
quadratic in the movement parameter, the same algebra as a ray against a
sphere, with the two radii added.
