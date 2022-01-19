# AVL tree

A binary search tree that rebalances itself after every change.

| Operation | Cost |
|---|---|
| Insert | O(log n) guaranteed |
| Search | O(log n) guaranteed |
| Delete | O(log n) guaranteed |
| Ordered traversal | O(n) |

| | |
|---|---|
| Memory | O(n), plus a height per node |
| Ordered | yes |

## The idea

Adelson-Velsky and Landis, 1962, the first self-balancing tree. The invariant is
deliberately strict: at every node the two subtree heights differ by at most one.

That forces the height to stay within about 1.44·log₂(n), so every operation is
logarithmic on every input, including the sorted one that turns a plain BST into a
list. **Measured here:** 1000 sorted keys give height 10, against 1000 for the
unbalanced tree and 17 for the red-black tree.

## How it works

After an insert or delete, walk back up recomputing heights. Where the balance
factor leaves [-1, 1], rotate.

There are four cases and really two. Left-left and right-right need one rotation.
Left-right and right-left need two, because the inner subtree has to be
straightened before it can be lifted.

## The trade

Shallower than a red-black tree, so lookups are faster, and it rebalances more often, so writes are slower. Read-heavy workloads take AVL; write-heavy ones take red-black.

## Where it is used

In-memory indexes and anywhere lookups dominate updates. Windows NT's virtual memory used AVL trees.
