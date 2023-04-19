# Bridges and articulation points

The single edges and vertices that hold a graph together.

| | |
|---|---|
| Time | O(V + E) |
| Memory | O(V) |
| Needs | an undirected graph |
| Answers | single points of failure |

## The idea

Both answers come from the same two numbers per vertex: the entry time and the
low-link, the earliest entry reachable from its subtree using at most one back
edge.

An edge from parent to child is a **bridge** exactly when
`low[child] > entry[parent]`: nothing in the child's subtree can reach the parent
or higher by another route.

A vertex is an **articulation point** when some child satisfies
`low[child] >= entry[vertex]`. The root is one when it has more than one child in
the search tree, since those subtrees meet only through it.

The whole difference between the two answers is `>` against `>=`. A child that can
reach exactly this vertex but no higher still leaves the graph connected if the
edge goes, and disconnects it if the vertex goes.

## How it works

One depth-first pass computing entry times and low-links, then reading the two conditions off. Written iteratively, since the recursion depth is the graph's depth.

## Where it is used

Auditing networks for single points of failure, planning redundancy, and as a building block for biconnected components and planarity testing.
