# Tree sort

Insert everything into a binary search tree, then walk it in order.

| | |
|---|---|
| Best | O(n log n) |
| Average | O(n log n) |
| Worst | O(n²) unbalanced |
| Memory | O(n) |
| Stable | yes |
| Family | insertion |

## The idea

An in-order traversal of a BST visits keys in ascending order, so sorting is just
building the tree and reading it back. The insert is the same comparison-and-descend
that insertion sort does linearly, except the tree lets it skip half the candidates
each step.

The catch is the shape. Sorted input builds a tree that is one long chain, and the
sort degrades to n². Replacing the plain BST with an AVL or red-black tree fixes
that and makes the n log n a guarantee, which is precisely why balanced trees exist.

## How it runs

1. Insert each element, descending left for smaller keys and right for larger.
2. Equal keys are collected in one node in arrival order, which keeps it stable.
3. Walk the tree in order and read out the values.

## When it is the right choice

When the tree is wanted anyway: if you are going to query, insert and delete afterwards, the sort is free. As a pure sort it is dominated by merge sort.
