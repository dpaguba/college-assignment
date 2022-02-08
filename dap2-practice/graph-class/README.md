# Graph class

Edge, Node and Graph for weighted directed graphs. Practical sheet 10, task 10.1.

```
java GraphDemo
Knoten: 4
Kanten: [0---4---1, 0---1---2, 2---7---3]
```

The sheet asks for the three classes without a main method; `GraphDemo` only
exercises them.

## Adjacency list, not matrix

The outgoing edges live at the node. Memory is O(n + m) instead of O(n²), and
iterating over one node's neighbours costs its degree rather than n. For the
sparse graphs the next tasks run on, that is the whole difference. A matrix
wins only when the graph is dense or when "is there an edge from i to j" has to
be O(1), and Floyd-Warshall on [sheet 12](../floyd-warshall/) is exactly that
case.

## Two costs stated rather than hidden

`getNode` is a linear scan, so every lookup is O(n) and building a graph from m
edges is O(n·m). A HashMap from id to node would make it O(1). `Node.addEdge`
also scans its list to reject a duplicate destination, so adding all edges of
one node is O(degree²).

Both are what the sheet prescribes, and both keep the edges in exactly the order
they were read, which the expected outputs on the following sheets depend on.

## Weights

The constructor rejects a weight of zero or less. Dijkstra needs that on the
next task, and the file format guarantees it.

## Verification

`GraphDemo` checks that duplicate ids are rejected, that a second edge to the
same destination is rejected, that an edge to a missing node is rejected, and
that a non-positive weight throws.
