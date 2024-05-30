# Graph basics

The second exercise sheet gives a digraph on the vertices 0 to 14 with 22
edges. Order 15, size 22, one source (0) and one sink (14), all of which
networkx confirms.

## It is not acyclic

The cycle is 4 → 6 → 13 → 4. Removing one edge of it, the one that leads
back, is enough: `make_acyclic` removes exactly one edge and the result
passes the acyclicity test. That answers the exercise's question of how the
graph would have to be modified.

If the vertices are process steps and the edges dependencies, the cycle is
not a drawing problem but a specification problem: no execution order exists
while it is there. That is the reason a layered drawing has to remove cycles
before it can assign layers at all.

## Storage

The adjacency matrix has one entry per edge, which the tests check by summing
it. It costs the square of the vertex count regardless of how many edges
there are; the adjacency list used here costs the number of edges.
