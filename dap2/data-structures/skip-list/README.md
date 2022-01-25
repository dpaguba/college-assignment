# Skip list

A linked list with express lanes, balanced by coin flips.

| Operation | Cost |
|---|---|
| Insert | O(log n) expected |
| Search | O(log n) expected |
| Delete | O(log n) expected |
| Ordered traversal | O(n) |

| | |
|---|---|
| Memory | O(n) expected, two pointers per node on average |
| Ordered | yes |

## The idea

A sorted linked list needs n steps to find anything, because there is no way to
skip. A skip list adds lanes above it: every node is on level 0, half on level 1, a
quarter on level 2. A search runs along the highest lane until the next node
overshoots, drops a level, and repeats, covering the list in log n steps.

The levels come from coin flips at insertion time, not from any rule about the data.
There is no rebalancing, no rotation and no case analysis: the expected shape is
good regardless of insertion order, and a bad shape needs a run of bad luck rather
than a bad input.

Pugh's 1990 paper argues for it almost entirely on how much easier it is to
implement correctly than a balanced tree. Anyone who has written red-black delete
agrees.

## How it works

Each node carries an array of forward pointers, one per level it reached. A search
records the last node it passed on every level, which is exactly the set of pointers
an insert or delete has to rewire.

## The trade

Expected rather than guaranteed logarithmic, and it uses more pointers than a tree. In return the code is a third of the length and an insert touches a handful of pointers with no rotations, which makes lock-free versions practical.

## Where it is used

Redis sorted sets, LevelDB and RocksDB memtables, and Lucene's term dictionaries.
