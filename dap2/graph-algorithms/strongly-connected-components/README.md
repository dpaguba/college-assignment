# Strongly connected components

The groups where everyone can reach everyone else.

| | |
|---|---|
| Time | O(V + E) |
| Memory | O(V) |
| Needs | a directed graph |
| Answers | the components, and implicitly the acyclic graph they form |

## The idea

Contract each strongly connected component to a point and any directed graph
becomes acyclic. That is why this is the first step in almost any analysis of a
directed graph: it separates the part that can be ordered from the part that cannot.

**Tarjan** does it in one pass using the low-link number: the smallest entry time
reachable from a vertex's subtree using at most one backward edge. When a vertex's
low-link equals its own entry time, nothing beneath it escapes to an earlier
vertex, so it is the root of a component and everything above it on the stack
belongs to that component.

**Kosaraju** does it in two passes with an argument you can hold in your head.
Record the finishing order, reverse every edge, then search again taking roots in
decreasing finishing time. Reversing leaves the components unchanged, because
mutual reachability is symmetric, but cuts every route between them.

Twice the work and a fraction of the explanation, which is why Kosaraju is the one
that gets taught and Tarjan's is the one that gets used.

## How it works

Both written iteratively. Tarjan carries a stack of open vertices and pops a component when it finds a root; Kosaraju runs two plain searches with a reversed graph in between. The tests check that both agree on every fixture.

## Where it is used

Deadlock detection, dependency cycle diagnosis, the 2-SAT algorithm, compiler optimisation over the call graph, and finding communities in link graphs.
