# Floyd-Warshall

All pairs shortest paths. Practical sheet 12, task 12.2.

```
java ShortestPaths fw < ../bellman-ford/positiv.graph
     0     -1      2      2      3
     3      0      5      3      4
     0     -3      0      0      1
     0     -1      2      0      1
    -1     -2      1      1      0
```

Needs the harness from the previous task:

```
javac -sourcepath ../bellman-ford -d out FloydWarshall.java ../bellman-ford/*.java
java -ea -cp out ShortestPaths fw < ../bellman-ford/positiv.graph
```

## The loop order is the algorithm

The outer loop over k means: allow paths whose interior nodes all come from
{0..k}. Each cell then asks whether routing through k beats what was known
without it. Putting k inside would ask that question before the answers it
depends on exist, and the result would be silently wrong on some inputs while
looking fine on most. It is the classic way to get this algorithm wrong.

Θ(n³) time, Θ(n²) space, four lines of code.

## Why the table is two-dimensional

It is dynamic programming over the set of allowed intermediate nodes, so the
natural table has three dimensions. The third is dropped because row k of the
new layer equals row k of the old one, which is what makes the update safe in
place.

## Against the alternatives

Running Dijkstra from every node is O(n·m log n) and wins on sparse graphs, but
cannot take negative edges. Running Bellman-Ford n times can, at O(n²·m), which
is worse on dense graphs, and the sheet explicitly forbids it: the point of the
task is the loop above, not the answer.

## Negative cycles

A negative entry on the diagonal after the main loop means that node lies on a
negative cycle. Every pair that can route through such a node then has no finite
distance and is marked MIN_WEIGHT in a final pass.

## Verification

Checked against [Bellman-Ford](../bellman-ford/) on 800 random graphs with
negative weights, including 280 with negative cycles: row 0 of this matrix
agreed with that algorithm's output in every entry.
