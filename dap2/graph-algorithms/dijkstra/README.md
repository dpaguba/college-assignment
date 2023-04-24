# Dijkstra's algorithm

Breadth-first search with a priority queue instead of a queue.

| | |
|---|---|
| Time | O(E + V log V) with a binary heap |
| Memory | O(V) |
| Needs | non-negative weights |
| Answers | cheapest path from one source |

## The idea

BFS spreads by edge count, so it is right only when every edge costs the same.
Replace the queue with a priority queue keyed by distance and the wave spreads by
cost instead. That substitution is the entire algorithm.

Correctness rests on one assumption: when a vertex comes off the queue, no cheaper
route to it can still appear. That holds because every edge adds a non-negative
amount, so any unfinished route is already at least as expensive.

**A single negative edge breaks the argument**, and Dijkstra then returns a wrong
answer confidently. This implementation raises instead, because a confident wrong
answer is worse than a refusal. Bellman-Ford is the algorithm for that case.

## How it works

Push the start at distance zero. Pop the cheapest vertex, mark it finished, and
relax its edges.

Python's heapq cannot decrease a key, so an improved distance is pushed as a second
entry and the stale one is skipped when it surfaces. That is the standard lazy
variant, and it is why a vertex may appear in the queue more than once.

## Where it is used

Routing protocols (OSPF, IS-IS), navigation software, network latency planning, and as the base A* specialises.
