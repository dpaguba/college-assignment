# Transitive closure

Two ways to the same answer. A search from every vertex collects what it can
reach; Warshall's algorithm lets each vertex serve once as an intermediate
station and fills the matrix in cubic time.

Both are computed on the exercise digraph and compared with each other, and
both are compared with `networkx.transitive_closure` on 40 random graphs.

The closure of a cycle is complete on that cycle: every vertex reaches every
other, including itself. Applying the closure again changes nothing, which is
what makes it a closure.

## The other direction

The transitive reduction removes every edge that is already implied by a
detour. It is unique only for acyclic graphs, so the function refuses a graph
with a cycle rather than returning one of several possible answers.
