# Binary search tree exercises

Not from the practical sheets: these two exercise methods appear in none of
the surviving course material, and are kept here because they were worth
finishing.

Two methods on a search tree, plus the tree they need in order to run.

```
java BinarySearchTree
size: 9
nodes at depth 0..1: 3
nodes at depth 2..3: 6
the four smallest:
20 30 35 40
```

## The empty tree is an object

An empty tree here is a node with no value, not a `null` reference. That costs
two extra objects per leaf and buys the property both exercises depend on:
`leftChild.countNodes(...)` is always a legal call, so the recursion never
tests for null and the base case lives in exactly one place.

This is the representation the course used, and both exercise methods were
written against it, so it was kept.

## Exercise 1: countNodes(top, bottom)

Count the nodes whose depth falls between `top` and `bottom`, with the root at
depth 0.

Descending one level shifts the window by one, so the recursion passes
`top - 1, bottom - 1` downwards and the test at each node is just whether 0 is
inside the window. The recursion stops as soon as `bottom` goes negative,
because everything below is deeper than the window and contributes nothing.
That is what keeps the cost proportional to the part of the tree the window
touches.

## Exercise 2: sortedUpTo(k)

Print the k smallest values in ascending order.

An in-order walk visits a search tree in sorted order, so the k smallest values
are the first k nodes it reaches. The return value carries how many are still
wanted, which is what lets the recursion stop in the middle of the tree instead
of walking all of it and discarding the tail.

O(h + k), not O(n). Printing the three smallest of a million values descends to
the leftmost leaf and stops.

## Verification

Two thousand random trees. `countNodes` was checked against depths computed
independently by replaying the insertion order into a plain map, for every
window from −2 to 7 including inverted ones. `sortedUpTo` was checked against
the sorted prefix for every k from 0 to size + 2, with `System.out` captured.

## What was wrong with the original

It was a fragment: the class declared no fields and no constructor, so
`content`, `leftChild`, `rightChild` and `isEmpty()` were all undefined and the
file did not compile.

`sortedUpTo` was also wrong where it did exist. It passed the full count down
the left subtree and then tested the returned value against zero to decide
whether to print, which stops one element early and prints nothing at all once
the left subtree is deep enough. The corrected version decrements after
printing and passes the remainder to the right subtree.

## Related

[binary-search-tree](../../dap2/data-structures/binary-search-tree/) in the
data structures library, along with the
[AVL](../../dap2/data-structures/avl-tree/) and
[red-black](../../dap2/data-structures/red-black-tree/) trees that fix the
degeneration this one has on sorted input.
