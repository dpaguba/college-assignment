# A*

Dijkstra that also uses an estimate of the distance still to go.

| | |
|---|---|
| Time | depends on the heuristic |
| Memory | O(V) |
| Needs | non-negative weights and an admissible estimate |
| Answers | cheapest path to one target |

## The idea

Dijkstra expands the cheapest vertex so far, which means it spreads in every
direction equally, including away from the goal. A* orders the queue by cost so far
plus an estimate of the cost remaining, so the search leans towards the target.

The estimate has to be **admissible**: never an overestimate of the true remaining
cost. Under that condition A* returns the same answer Dijkstra would, having looked
at fewer vertices. Overestimate and it becomes fast and wrong, which is the trade
greedy best-first search makes deliberately.

With the estimate returning zero, the formula reduces to Dijkstra exactly. That is
the cleanest way to see what A* is: not a different algorithm, but the same one
with a better queue order, and the test suite checks that both give the same cost.

## How it works

A priority queue keyed by `cost so far + estimate`. Everything else is Dijkstra.

**A measured caveat.** On a uniform grid, Manhattan distance to the opposite corner
is exact, so every cell lies on some shortest path and both searches expand
everything: 400 of 400 vertices on a 20 by 20 board. Move the goal near the start
and the difference appears at once, 4 vertices against 10. The heuristic helps by
ruling cells out, and when nothing can be ruled out it helps not at all.

## Where it is used

Game pathfinding, robotics, route planning with geographic distance as the estimate, and puzzle solving where the heuristic is a relaxation of the puzzle.
