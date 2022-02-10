# Prim and Kruskal

Minimum spanning trees, and the union-find structure Kruskal needs. Practical
sheet 11.

```
java Prim < BspGraphKlein.graph
[0---1---1, 1---3---2, 2---3---5, 3---4---5, 3---6---4]
Gewicht des minimalen Spannbaums: 17
```

`java Kruskal < BspGraphKlein.graph` prints the same tree. The edge format is
`src---weight---dst`.

## UnionFind, as the sheet prescribes it

A list per set, plus a map from node to its list. The map is what makes `find`
O(1) instead of a search through every list.

`union` appends the smaller list to the larger one. Which one survives matters:
appending the larger to the smaller would update more map entries and lose the
bound. As written, a node can only move when its set at least doubles, so it
moves at most log n times and m unions cost O(m log m) in total.

The classical union-find with parent pointers, union by rank and path
compression is faster still, at inverse Ackermann per operation, which is
effectively constant. The list version is what the sheet asks for and it makes
"what is a set here" obvious.

## The two algorithms

**Kruskal** sorts the edges and takes every one that joins two different
components. O(m log m), dominated by the sort.

**Prim** grows a single tree, always adding the cheapest edge leaving it, using
the priority queue. O((n + m) log n) with a binary heap. A Fibonacci heap brings
it to O(m + n log n), which is one of the few places that structure genuinely
helps.

They differ in what they grow: Kruskal a forest that only becomes connected at
the end, Prim one tree from the start. Both are correct for the same reason, the
**cut property**: for any split of the nodes into two groups, the lightest edge
crossing it belongs to some minimum spanning tree. Kruskal's next accepted edge
is the lightest across the cut between the component it joins and the rest;
Prim's is the lightest across the cut between the tree and everything else.

## Disconnected input

Prim's queue hands back a node with an infinite key, and Kruskal ends with more
than one set. Both print `Graph nicht zusammenhaengend!`.

## Output order

The tree is printed with each edge oriented from the smaller id to the larger
and sorted by weight, so the output does not depend on the order the search
happened to visit the nodes. That is what reproduces the sheet's expected line
exactly.

## The provided classes

`VorgabenBlatt11.zip` was not in the surviving material, so `Graph`, `Node`,
`Edge`, `MinPQ` and `HeapElement` here are reimplementations of the interface
listed on the supplementary sheet. They differ from the ones in
[graph-class](../graph-class/): these are undirected, storing each edge twice
with the halves linked as siblings, and they can read a graph from standard
input. `TooManyElementsException` belongs to the course's own queue
implementation and has no counterpart here.

`BspGraphKlein.graph` was reconstructed so that its minimum spanning tree is
exactly the one the sheet prints, weight 17 included.

## Verification

The expected Prim output, matched exactly, and Kruskal agreeing on the same
graph. Beyond that, 400 random connected graphs where Prim, Kruskal and a brute
force over all spanning trees all agreed on the weight.
