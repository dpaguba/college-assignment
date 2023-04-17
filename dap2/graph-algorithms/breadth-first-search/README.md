# Breadth-first search

Visit everything one step away, then two, then three.

| | |
|---|---|
| Time | O(V + E) |
| Memory | O(V) |
| Needs | nothing |
| Answers | shortest path in edge count, level order |

## The idea

A queue is the whole algorithm. Because vertices come out in the order they went
in, everything at distance one is processed before anything at distance two, and
the wave spreads outward evenly.

That single property is why BFS finds shortest paths in an unweighted graph, and
why it stops being correct the moment edges have different weights: the wave
measures edges crossed, not distance travelled. Dijkstra is this algorithm with the
queue replaced by a priority queue, which is exactly the fix.

## How it works

Queue the start, then repeatedly take a vertex and queue its unseen neighbours.

Mark a vertex when it is **queued**, not when it is dequeued. Marking on dequeue
lets a vertex enter the queue through several neighbours, and on a dense graph that
is the difference between linear and quadratic.

The parent map falls out of the same sweep: each vertex remembers who reached it
first, and first means closest, so following parents back from the goal gives a
shortest path with no extra work.

## Where it is used

Shortest routes in unweighted graphs, web crawlers, flood fill, finding connected components, and the level order traversal of any tree.
