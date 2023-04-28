# Prim's algorithm

Grow one tree, always taking its cheapest edge to the outside.

| | |
|---|---|
| Time | O(E + V log V) with a heap |
| Memory | O(V) |
| Needs | undirected weighted graph, a start vertex |
| Answers | minimum spanning tree of one component |

## The idea

Kruskal considers edges everywhere and keeps a forest that only becomes a tree at
the end. Prim keeps one tree from the first step and asks a narrower question each
time: which single edge leaving the tree is cheapest.

Both rest on the same cut property, applied to different cuts. Kruskal takes the
cheapest edge across whatever split that edge repairs; Prim takes the cheapest edge
across the split between the tree and everything else. Same guarantee, different
bookkeeping.

It is Dijkstra with one change: the priority is the edge weight rather than the
distance from the source. Everything else, the heap, the stale entries, the
frontier, is identical.

## How it works

A priority queue over the frontier edges. Stale entries, where the far end has already joined, are skipped rather than removed. Prim needs a start and only reaches its component, where Kruskal covers the whole graph unasked.

## Where it is used

Dense graphs, where it beats Kruskal because Kruskal must sort every edge whether or not it is used. Also the basis of several approximation algorithms for the travelling salesman problem.
