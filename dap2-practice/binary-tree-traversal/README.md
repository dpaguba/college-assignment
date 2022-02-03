# Binary tree traversal

A search tree built from CSV input, printed in one of three orders. Practical
sheet 8, task 8.1.

```
java SearchTreeApplication < sample1.csv
Hoehe: 6
-10 -5 3 4 5 11 12 13 17 40 100
Hoehe: 13
1 2 3 4 5 6 7 8 9 10 11 12 13
Hoehe: 4
1 2 3 5 6 7 9 10 11 12 14 15 16 17 20
```

The first line of the file names the traversal; an optional command line
argument overrides it (`java SearchTreeApplication pre < sample1.csv`).

## The three orders

**In-order** visits left, node, right, which on a search tree is sorted order.
**Pre-order** visits the node first, and replaying it as an insertion sequence
rebuilds exactly the same tree, which is what makes it the useful one for
serialising. **Post-order** finishes both children before the node, which is
what you want when the visit destroys the node.

An in-order and a post-order traversal together determine the tree uniquely.
That is not decoration here: the sample files were reconstructed from the
expected outputs on the sheet, which give in-order for one file and post-order
for the same trees in another.

## Height

The height attribute is updated on the way out of each insertion, so reading it
is O(1) rather than O(n).

The sheet's hint says a leaf has height 0, and every expected output on the
sheet is one larger than that convention gives: the chain of 13 ascending values
has 12 edges and the output says 13. So height here counts nodes, not edges: an
absent subtree is 0 and a leaf is 1. Where the hint and the expected output
disagree, the output wins.

## The second line of the sample file

Thirteen values inserted in ascending order give a tree of height 13, a linked
list with extra pointers. That is the worst case of every search tree operation
and the entire motivation for the [AVL tree](../avl-tree/) on the next task.

## The sample files

`VorlagenBlatt08.zip` was not in the material that survived, so `sample1.csv`
and `sample3.csv` were reconstructed from the expected outputs by rebuilding
each tree from its in-order and post-order traversals and reading off a valid
insertion sequence. Both files reproduce the sheet's output exactly, heights
included, which is the check that the reconstruction was right.

## Verification

Both sample outputs, line for line, plus all four error cases.
