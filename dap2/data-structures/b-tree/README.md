# B-tree

Many keys per node, shaped so one node fills one page of storage.

| Operation | Cost |
|---|---|
| Insert | O(log_t n) |
| Search | O(log_t n) |
| Delete | O(log_t n) |
| Ordered traversal | O(n) |

| | |
|---|---|
| Memory | O(n) |
| Ordered | yes |

## The idea

A binary tree over a million keys is twenty levels deep, and if each level is a
separate disk page that is twenty seeks. A B-tree of degree 100 holds the same
million keys in three levels, so the same lookup costs three reads. The comparison
count barely changes; the number of pages touched collapses, and that is the number
that decides how long the query takes.

**Measured here**, 10000 keys:

| Structure | Height |
|---|---|
| AVL tree | 14 |
| B-tree, degree 2 | 13 |
| B-tree, degree 3 | 8 |
| B-tree, degree 50 | 3 |
| B-tree, degree 100 | 2 |

## How it works

A node holds between t-1 and 2t-1 keys and one more child than keys. Nothing
rotates. A node that overflows splits in two and pushes its middle key up; a node
that underflows borrows from a sibling or merges with one.

Because growth happens at the root rather than at the leaves, every leaf sits at the
same depth by construction. The test checks exactly that, plus the key limits, after
every one of 800 random operations.

## The trade

Wider nodes mean fewer levels and more comparisons per level, which is the right trade when a level costs a disk seek and a comparison costs nothing. In pure memory a binary tree is usually better.

## Where it is used

Every relational database index, the filesystems NTFS, HFS+, ext4 and btrfs, and most key-value stores. B+ trees, which keep all values in the leaves and link them, are the variant databases actually use for range scans.
