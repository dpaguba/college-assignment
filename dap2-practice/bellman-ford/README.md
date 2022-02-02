# Bellman-Ford

Single source shortest paths with negative weights. Practical sheet 12, task
12.1.

```
java ShortestPaths bf < positiv.graph
d(0, 0) = 0
d(0, 1) = -1
d(0, 2) = 2
d(0, 3) = 2
d(0, 4) = 3
```

The file format is n on the first line, m on the second, then m lines of
`u v w`.

## The algorithm

Relax every edge, n − 1 times. After round k every shortest path using at most k
edges has been found, and without negative cycles a shortest path uses at most
n − 1 edges. O(n·m).

The improvement the sheet asks for is the early exit: if a full round changes
nothing, no later round can change anything either, because every relaxation
depends on a value that changed in the round before. On most inputs that ends
the loop long before n − 1 rounds.

## Against Dijkstra

O(n·m) against O(m log n). The price buys negative edges, which
[Dijkstra](../dijkstra/) cannot handle at all: its argument for settling the
nearest node assumes no edge can shorten a path.

## Negative cycles

One extra round after the loop. Anything that still improves lies on or behind
a negative cycle, and then **everything reachable from it** has no finite
shortest path, so MIN_WEIGHT is propagated forward with a breadth-first walk.

The direction matters and is the part that is easy to get wrong: being
reachable *from* the cycle is what makes a distance unbounded, not lying on it
or reaching it.

Three outcomes, as the sheet specifies: MAX_WEIGHT when there is no path,
MIN_WEIGHT when there is a path but no shortest one, and the weight otherwise.

## The harness

`ShortestPaths.java` was provided by the course and was not in the surviving
material, so it is reimplemented here from the file format the sheet describes.
It also holds the `Edge` class and the two sentinel constants, which is why
[floyd-warshall](../floyd-warshall/) compiles against this folder.

## Verification

800 random graphs with negative weights, 280 of them containing a negative
cycle, where the distance vector agreed with row 0 of Floyd-Warshall's matrix
in every entry, sentinels included.
