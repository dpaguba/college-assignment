# Depth-first search

Follow one branch to its end before trying the next.

| | |
|---|---|
| Time | O(V + E) |
| Memory | O(V) |
| Needs | nothing |
| Answers | reachability, entry and exit times, cycles |

## The idea

BFS and DFS differ by one data structure: a queue against a stack. Everything else
follows from that. BFS spreads evenly and measures distance; DFS plunges and
measures structure.

What DFS gives that BFS cannot is entry and exit times. Those two numbers per
vertex are the foundation of topological order, strongly connected components,
bridges, articulation points and cycle detection, all of which read the shape of
the search rather than its result.

The intervals nest: one vertex is an ancestor of another exactly when its interval
contains the other's, which turns questions about tree shape into arithmetic.

## How it works

Written with an explicit stack. The recursive form is shorter and dies on a graph
twenty thousand vertices deep, which is a chain, not an exotic case, and the test
suite checks exactly that.

Cycle detection uses three colours: white unvisited, grey on the current path,
black finished. Reaching a grey vertex means the path has looped. In an undirected
graph the way back to the parent is grey, so the parent is skipped explicitly.

## Where it is used

Cycle detection, topological sorting, connected and strongly connected components, maze generation, and the backtracking core of every constraint solver.
