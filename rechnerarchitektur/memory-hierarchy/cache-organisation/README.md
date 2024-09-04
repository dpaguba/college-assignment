# Cache organisation

An address splits into three fields: the **offset** picks a byte in a block,
the **index** picks the set, the **tag** is stored to check the block is the
one wanted.

A 1 KB cache with 32-byte blocks and two ways has 5 offset bits and 4 index
bits, and everything else is tag.

## The three parameters trade against each other

| change | removes | costs |
|---|---|---|
| bigger block | compulsory misses, through spatial locality | bandwidth when locality is poor |
| more ways | conflict misses | comparators and hit time |
| bigger cache | capacity misses | hit time |

Each is measured rather than asserted. A direct-mapped 64-byte cache with
16-byte blocks evicts address 0 when address 64 arrives, and a two-way cache of
the same size does not. A stride-4 stream through 64 bytes misses far less with
32-byte blocks than with 4-byte blocks, because one miss brings in eight
subsequent accesses.
