# Binary search tree

Chapters seven and twelve, and the exam tasks from the extra sheets.

The representation is the course's: every subtree is a tree object and an
empty tree is an object whose content is null. That is why the recursive
methods never test a child for null and always call the child, and it is what
the exam tasks assume.

## Insertion order decides everything

Depth of a tree holding 1023 values:

| | depth |
|---|---:|
| built balanced from the sorted values | 10 |
| inserted in ascending order | 1023 |
| inserted in random order | 23 |

The same values, the same insert method, and a structure that is either a
tree or a linked list depending on the order they arrived in. Every operation
here is proportional to the depth, so the sorted insertion turns a logarithmic
structure into a linear one, and it does so on the input a user is most likely
to have lying around.

Random insertion gives 23, about twice the optimum, which is the usual result:
random trees are logarithmic with a constant of roughly two. Guaranteeing the
optimum needs rebalancing, which this course leaves to its successor.

## Deletion

Three cases, and only the third is interesting. A leaf is dropped, a node with
one child is replaced by that child, and a node with two children keeps its
position and takes the smallest value of its right subtree. That value is the
next one in order, so it is the only value that can stand there without
breaking the order condition, and it has no left child, so removing it from
where it was is one of the two easy cases.

Checked against `java.util.TreeMap` over 60 trials of 60 random insertions and
deletions each.

## The exam tasks

The extra sheets are exam questions from previous years, given as method
skeletons to complete. They are implemented here on the same class:

| | |
|---|---|
| `countNodes(top, bottom)` | nodes on the levels between two bounds, skipping levels that do not exist |
| `largestOn(level)` | the largest value on one level |
| `maxOfLess(bound)` | the largest value below a bound |
| `sortedUpTo(n)` | the smallest n values, in order |
| `subTree(value)` | the subtree rooted at a value |

`maxOfLess` is the one where the order condition pays: a node at or above the
bound rules out its entire right subtree, so the search is a path rather than
a traversal. `largestOn` is the opposite case, since the order condition says
nothing about a level, so every node on it has to be looked at.
