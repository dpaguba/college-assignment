# Binary heap

A tree kept in a flat array, where every parent is smaller than its children.

| Operation | Cost |
|---|---|
| Push | O(log n) |
| Pop the minimum | O(log n) |
| Peek | O(1) |
| Build from a list | O(n) |

| | |
|---|---|
| Memory | O(n), contiguous, no pointers |
| Ordered | partially: only parent before child |

## The idea

A sorted array gives the minimum instantly and costs n per insert. An unsorted array
inserts instantly and costs n to find the minimum. A heap gives log n for both, and
that compromise is what made Dijkstra's algorithm practical.

The trick is that a heap is not sorted, only partially ordered: a parent is smaller
than its children and nothing is known about siblings. Maintaining nothing between
siblings is exactly what keeps both operations logarithmic.

There are no nodes and no pointers. The tree lives in an array, children of i at
2i+1 and 2i+2, so the structure is arithmetic rather than allocation.

## How it works

Push appends at the end and sifts up while it is smaller than its parent. Pop takes
the root, moves the last element there, and sifts it down.

Building from an existing list costs O(n), not O(n log n). The proof is a sum over
levels: half the nodes are leaves and sift no distance, a quarter sift one, and the
series converges. That bound surprises people and is a standard exam question.

## The trade

It answers only one question, what is the smallest, and answers it well. It cannot search, cannot iterate in order without destroying itself, and cannot change a key's priority without knowing where that key sits.

## Where it is used

Priority queues everywhere: Dijkstra and A*, task schedulers, event simulation, Huffman coding, and heapsort. Python's `heapq` is this structure.
