# Dijkstra

Shortest path between two nodes. Practical sheet 10, task 10.2.

```
java DijkstraApplication < BspGraphKlein0-4.graph
Kuerzester Pfad 0, 2, 4 mit Laenge 5 gefunden.
```

Needs the graph classes from the previous task:

```
javac -sourcepath ../graph-class -d out *.java
java -ea -cp out DijkstraApplication < BspGraphKlein0-4.graph
```

## The algorithm

Keep tentative distances in a min-priority queue, repeatedly settle the nearest
unsettled node, relax its outgoing edges. O((n + m) log n) with a binary heap.

Settling the nearest unsettled node is safe **because all weights are
positive**: any other route to it would have to leave through a node at least as
far away, so it could only be longer. One negative edge and that argument
collapses, which is why [Bellman-Ford](../bellman-ford/) exists.

The search stops when the target comes out of the queue, not when the queue
empties. A settled node's distance is final, so everything after that is
computed for nothing.

## decrease-key

The queue's interesting operation is lowering a key in the middle of the heap,
which a plain binary heap cannot do: it has no way to find the element. The map
from node id to array index is what makes it possible, and keeping that map
correct through every swap is the only real work in `MinPQ`.

The alternative used in most short implementations is to push a duplicate entry
and skip stale ones on extraction. It is simpler and costs O(m log m) instead of
O(m log n), which is the same thing up to a constant.

## The result

`dijkstra` returns the path as a graph, not just its length, rebuilt by walking
the predecessor map back from the target.

## The sample files

`VorlagenBlatt10.zip` was not in the surviving material, so `MinPQ`,
`HeapElement` and `DijkstraResult` are reimplementations of the interfaces the
sheet describes, and the `.graph` files were written here. They are built to
reproduce the two expected outputs on the sheet exactly, including
`Kuerzester Pfad 2, 14, 16, 5, 25, 27 mit Laenge 13 gefunden.`

## Verification

Both expected outputs, the unreachable case, and all six error messages.

Beyond the sheet: 500 random graphs, every source-target pair, checked against
Floyd-Warshall, with every returned path also walked edge by edge to confirm it
exists and has the claimed length.
