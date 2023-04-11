# Graph algorithms

Fourteen algorithms, one folder each, in plain Python with no dependencies.
Every folder holds the implementation and a README explaining the idea, how it
works and where it is used.

They all take the same small `Graph` from [graph.py](graph.py), an adjacency
list with optional weights and direction. Adjacency list rather than matrix: a
matrix costs V² memory and answers "is there an edge" in O(1), a list costs
V + E and answers "what are the neighbours" in O(degree). Almost every
algorithm here asks the second question, and almost every real graph is sparse.

## Traversal

| Algorithm | Time | Answers |
|---|---|---|
| [breadth-first-search](breadth-first-search/) | O(V + E) | shortest path in edges, level order |
| [depth-first-search](depth-first-search/) | O(V + E) | reachability, entry and exit times, cycles |

## Shortest paths

| Algorithm | Time | Handles | Solves |
|---|---|---|---|
| [dijkstra](dijkstra/) | O(E + V log V) | non-negative weights | one source |
| [bellman-ford](bellman-ford/) | O(V·E) | negative weights, finds negative cycles | one source |
| [dag-shortest-path](dag-shortest-path/) | O(V + E) | any weights, acyclic only | one source, and longest too |
| [floyd-warshall](floyd-warshall/) | O(V³) | negative weights | every pair |
| [a-star](a-star/) | heuristic dependent | non-negative, needs an estimate | one target |

## Spanning trees

| Algorithm | Time | Idea |
|---|---|---|
| [kruskal](kruskal/) | O(E log E) | sort the edges, skip the ones that close a cycle |
| [prim](prim/) | O(E + V log V) | grow one tree by its cheapest outgoing edge |
| [boruvka](boruvka/) | O(E log V) | every component picks at once, parallel friendly |

## Structure

| Algorithm | Time | Answers |
|---|---|---|
| [union-find](union-find/) | O(α(n)) per operation | are these two connected |
| [topological-sort](topological-sort/) | O(V + E) | an order respecting all dependencies |
| [strongly-connected-components](strongly-connected-components/) | O(V + E) | who can reach whom, both ways |
| [bridges-and-articulation-points](bridges-and-articulation-points/) | O(V + E) | single points of failure |

## The one thing that connects them

Half of this folder is the same idea wearing different clothes.

**BFS, Dijkstra and A\* are one algorithm with three queue orders.** A plain
queue measures edges. A priority queue on distance measures cost. A priority
queue on distance plus an estimate leans towards a goal. Set the estimate to
zero and A* is Dijkstra; make every weight one and Dijkstra is BFS.

**Prim is Dijkstra with a different priority.** Distance from the source
becomes weight of the crossing edge, and a shortest path tree becomes a
minimum spanning tree.

**Kruskal, Prim and Borůvka all rest on the cut property**, applied to
different cuts: whatever cut the edge repairs, the cut between the tree and
the rest, and every component's own cut at once.

**Topological order, strongly connected components and bridges are all read
off DFS entry and exit times.** None of them needs machinery beyond those two
numbers per vertex.

## Choosing one

Unweighted shortest path: BFS. Weighted with non-negative edges: Dijkstra.
Negative edges, or you need to know a negative cycle exists: Bellman-Ford.
No cycles at all: the DAG pass, which is linear and takes negative weights
without complaint. Every pair on a dense graph: Floyd-Warshall. A known target
and a distance estimate: A*.

Spanning tree on a sparse graph: Kruskal. On a dense one: Prim. On many cores:
Borůvka.

## How this was built

Test first. Each algorithm got a test file before it had an implementation,
run to watch it fail for the right reason, then the code, then the run again.
The graphs live in [graph_fixtures.py](graph_fixtures.py) and each one exists
to break something specific: a disconnected graph, a negative edge, a negative
cycle, a directed cycle, a grid with walls.

Where two algorithms answer the same question, the tests check them against
each other rather than against a hand-written answer: Floyd-Warshall against
Dijkstra from every source, Prim and Borůvka against Kruskal, Tarjan against
Kosaraju, Kahn against the DFS topological sort.

Three things the tests caught. Bellman-Ford's path reconstruction was left
returning None, which no test had covered until one was written for it. A
spanning tree test asserted a total weight of 26 that had been invented rather
than computed; two independent implementations said 27, and working the edges
by hand agreed with them, so the test was wrong and not the code. And the
A* test assumed a good heuristic always explores less, which is false on a
uniform grid where the heuristic is exact and every cell lies on some shortest
path.

The tests were removed once all 66 passed, so what remains is the library and
the explanations.
