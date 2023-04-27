# Kruskal's algorithm

Sort the edges, take any that does not close a cycle.

| | |
|---|---|
| Time | O(E log E) |
| Memory | O(V) |
| Needs | undirected weighted graph |
| Answers | minimum spanning tree, or forest |

## The idea

Two lines of English: sort the edges by weight, take each unless it would close a
cycle.

Why that is optimal is the **cut property**. For any split of the vertices into two
groups, the cheapest edge crossing the split belongs to some minimum spanning tree.
Taking edges in increasing order means every edge taken is the cheapest across the
split it repairs, so nothing better was passed over.

The interesting part is "would close a cycle". Checking by traversal costs O(V) per
edge and the whole thing becomes O(E·V). Union-Find answers it in almost constant
time, so the sort dominates. This is the algorithm that made Union-Find worth
inventing.

## How it works

Sort, then one pass with a Union-Find. On a disconnected graph it produces a spanning forest rather than failing, which falls out of the method with no special case.

## Where it is used

Network design, clustering (single-linkage clustering is Kruskal stopped early), and image segmentation.
