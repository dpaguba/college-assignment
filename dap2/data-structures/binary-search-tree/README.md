# Binary search tree

Smaller keys left, larger keys right, all the way down.

| Operation | Cost |
|---|---|
| Insert | O(log n) average, O(n) worst |
| Search | O(log n) average, O(n) worst |
| Delete | O(log n) average, O(n) worst |
| Ordered traversal | O(n) |

| | |
|---|---|
| Memory | O(n) |
| Ordered | yes |

## The idea

The invariant is one sentence: everything in a node's left subtree is smaller than
the node, everything to the right is larger. Both the search, compare and descend,
and the ordered traversal, left then node then right, follow from it directly.

That ordering is what a hash table cannot give. A hash table answers "is this key
present" faster, and it cannot answer "what is the next key after this one" or
"give me everything between 10 and 20", because hashing destroys order on purpose.

**Measured here:** inserting 1000 sorted keys produces a tree of height 1000. The
AVL tree next door produces height 10 from the same input. The unbalanced tree is
not slower by a constant, it is a linked list wearing a tree's interface.

## How it works

Insert and search descend by comparison. Deletion has three cases: a leaf is
unlinked, a node with one child is replaced by it, and a node with two children is
replaced by its in-order successor, the smallest key in its right subtree, which is
the only key that can take its place without breaking the invariant.

`height` is walked with an explicit stack rather than recursion, because a tree
built from sorted keys is a chain n deep and recursing down it overflows the
interpreter stack. The structure would otherwise crash on precisely the input that
demonstrates its weakness.

## The trade

Simple enough to write correctly from memory, and it has no worst-case guarantee at all. Sorted or nearly sorted input, which is extremely common, is its worst case.

## Where it is used

Rarely on its own. It is the base every balanced tree modifies, and the structure every discussion of balancing starts from.
