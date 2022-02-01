# AVL tree

A search tree that rebalances itself. Practical sheet 8, task 8.2.

```
java AVLTreeApplication < sample2.csv
Fuege 15 in AVL-Baum ein.
Fuege 9 in AVL-Baum ein.
Fuege 7 in AVL-Baum ein.
Linker Teilbaum von "15" hat Hoehe 2. Rechter Teilbaum hat Hoehe 0.
Fuehre Rechts-Rotation durch
...
Hoehe: 4
19 9 7 15 17 21 20 27
----------
```

## The invariant

At every node the two subtree heights differ by at most one. That bounds the
height by about 1.44 log n, which turns the O(h) operations of a plain search
tree into O(log n) on every input.

## Why one repair is enough

A single insertion can only unbalance nodes on the path from the root to the new
leaf, and rebalancing the lowest such node restores the whole tree. So one or
two rotations always suffice and the insertion stays O(log n).

Four cases, decided by which side is heavy and which side of that child is heavy
in turn. Left-left and right-right need one rotation. Left-right and right-left
need the inner child rotated out of the way first, because a single rotation
would only move the problem across.

## Rotation without parent pointers

The rotations move contents rather than nodes: the object stays the parent's
child, so no parent pointer has to be updated and the class needs none. The
value of the pivot is copied up and the old contents are pushed into a new node
below.

## The question the sheet ends with

"Compare the heights for different inputs. Where is the difference largest?"
`HoehenVergleich` answers it with 1000 values:

| input | SearchTree | AVLTree |
|---|---|---|
| ascending | 1000 | 10 |
| shuffled | 24 | 12 |

Sorted input is the answer, and it is not a marginal difference: a factor of
100. On random input a plain search tree is already within a factor of two of
optimal, which is why the balancing is worth almost nothing there and
everything on sorted data. Sorted insertion is also the common case in
practice, since data usually arrives ordered by something.

Compile it against the previous task:

```
javac -sourcepath ../binary-tree-traversal:. -d out HoehenVergleich.java
java -ea -cp out HoehenVergleich 1000
```

## Verification

The whole trace for `sample2.csv` matches the sheet byte for byte: every
insertion line, the three imbalance reports with their heights, the rotation
names, the tree height, and the pre-order output. The assertion after each
insertion checks the AVL invariant everywhere.

`sample2.csv` was reconstructed from that expected trace, which lists the
insertion order explicitly.
