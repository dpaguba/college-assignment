# Union-Find

Which things are connected, answered in almost constant time.

| | |
|---|---|
| Time | O(α(n)) amortised per operation |
| Memory | O(n) |
| Needs | nothing |
| Answers | are these two in the same set |

## The idea

The question is deliberately narrow: not what a component contains, only whether
two things are in the same one. Giving up the first buys an answer to the second
that is faster than any traversal.

Each set is a tree and the root is its name. `find` walks to the root, `union`
points one root at another. On its own that degenerates into a chain, and two
refinements keep it flat:

**Union by rank** hangs the shorter tree under the taller, so height only grows
when two equal trees meet, which needs twice as many elements each time.

**Path compression** points every node passed during a `find` straight at the root,
so the next query on any of them is one step.

Together they give O(α(n)), where α is the inverse Ackermann function. It is below
5 for any n that could be stored in this universe, so the operations are constant
in every practical sense while not being constant in theory. That gap is why the
analysis is famous.

## How it works

Two arrays, parent and rank. `find` walks up then flattens; `union` compares ranks and links. The test checks that a chain of 10000 unions leaves a depth of at most 2 after one find, which is what proves compression is working.

## Where it is used

Kruskal's algorithm, image segmentation, network connectivity, Fortran's EQUIVALENCE, and every deduplication job that asks whether two records are the same entity.
