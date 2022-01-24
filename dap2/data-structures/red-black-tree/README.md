# Red-black tree

A search tree balanced by colours instead of by height.

| Operation | Cost |
|---|---|
| Insert | O(log n) guaranteed, at most 2 rotations |
| Search | O(log n) guaranteed |
| Delete | O(log n) guaranteed, at most 3 rotations |
| Ordered traversal | O(n) |

| | |
|---|---|
| Memory | O(n), plus one bit per node |
| Ordered | yes |

## The idea

Four rules do the work. The root is black; a red node has no red child; and every
path from a node to a missing child passes the same number of black nodes. From the
last two it follows that the longest path is at most twice the shortest, so the
height stays within 2·log₂(n+1).

That bound is weaker than AVL's, deliberately. A looser invariant is violated less
often, so an insert or delete needs a constant number of rotations rather than a
rebalance that may propagate to the root. Reads are marginally slower, writes
markedly faster.

**Measured here:** 1000 sorted keys give height 17, against AVL's 10. Both
logarithmic; AVL is tighter, red-black is cheaper to maintain.

## How it works

A fresh node is red, which can only break the "no red child of a red parent" rule.
Fixing it either recolours and moves the problem up, or rotates once and stops.

Deletion is the hard half: removing a black node breaks the equal-black-count rule,
and the deficit is carried up through four cases until a sibling can absorb it. A
single black sentinel stands in for every missing child, which is what keeps that
case analysis readable.

The test here checks all four rules after every one of 600 random operations,
because without them this is just a binary search tree with a colour field.

## The trade

More complex than AVL by some margin, particularly delete, in exchange for fewer structural changes per write.

## Where it is used

`std::map` and `std::set` in C++, `TreeMap` and `TreeSet` in Java, the Linux kernel's scheduler and virtual memory areas, and epoll.
