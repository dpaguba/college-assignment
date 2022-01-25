# van Emde Boas tree

O(log log u) by recursing on the size of the universe, not on the data.

| Operation | Cost |
|---|---|
| Insert | O(log log u) |
| Search | O(log log u) |
| Delete | O(log log u) |
| Successor or predecessor | O(log log u) |

| | |
|---|---|
| Memory | O(u), whether it holds ten keys or a billion |
| Ordered | yes |

## The idea

Every balanced tree here recurses on the number of elements: n keys, log n levels.
This one recurses on the size of the universe instead. A universe of u values splits
into √u clusters of √u values, and a query descends into one cluster, so the
universe is square-rooted at every step. Halving the exponent repeatedly gives
log log u.

The numbers are worth stating. Over 32-bit keys a balanced tree needs about 32
comparisons; this needs 5. Successor and predecessor cost the same, which a hash
table cannot do at all.

## How it works

A node stores a minimum, a maximum, an array of clusters and a summary structure
recording which clusters are non-empty.

Two details carry the bound. The minimum is held in the node and never inserted into
a cluster, so inserting into an empty cluster stops immediately. And each operation
makes only one recursive call rather than two, by consulting the summary to decide
where to go.

## The trade

The fastest known bound for successor queries over integer keys, at a memory cost proportional to the universe rather than the contents. That is why it is famous and rare.

## Where it is used

Almost nowhere directly. Y-fast tries reach the same time bound in O(n) space and are what gets used; this is the structure they are built to imitate.
