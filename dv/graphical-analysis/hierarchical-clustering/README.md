# Hierarchical clustering

Start with every point alone, repeatedly merge the two closest groups. What
"closest" means is the whole choice: the smallest distance between members
(single), the largest (complete), or the mean (average).

## Single linkage is the spanning tree

The merge distances of single linkage are exactly the edge lengths of the
minimum spanning tree in ascending order. The module builds the tree
independently with Prim's algorithm and compares; the two agree on 30 random
point sets.

## Shape against compactness

Eight points on two horizontal rows, neighbours 1 apart within a row, the
rows 1.5 apart. Cut to two groups:

- single linkage returns the two rows, because each row chains at distance 1
  and joining the rows costs 1.5;
- complete linkage cuts across, pairing the left halves of both rows against
  the right halves, because the ends of one row are 3 apart and that is worse
  than 1.8 across.

Neither is wrong. Single linkage follows connected shape and is the one that
chains; complete linkage insists on compact groups and will cut a long thin
one in half.
