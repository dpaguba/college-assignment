# The three Cs

Every miss is compulsory, capacity or conflict, and the classification is not a
label but a **measurement against two reference caches**:

| category | definition |
|---|---|
| compulsory | the block was never referenced before, so no cache would have it |
| capacity | a fully associative cache of the same size also misses |
| conflict | a fully associative cache of the same size would hit |

Only the third is an artefact of the organisation, and only the third is what
associativity removes.

## What the split says that a miss rate does not

Eight blocks cycled four times through a 64-byte cache with 16-byte blocks:

| ways | misses | compulsory | capacity | conflict |
|---|---|---|---|---|
| 1 | 32 | 8 | 24 | 0 |
| 2 | 32 | 8 | 24 | 0 |
| 4 | 32 | 8 | 24 | 0 |
| 8 | **8** | 8 | 0 | 0 |

Associativity does nothing here until the cache can hold the whole working set,
because the misses were never conflicts. Reading only the miss rate would
suggest the mapping is at fault; the split says the size is.

The reverse case is also measured: alternating between two addresses that share
an index gives conflict misses in a direct-mapped cache and none at full
associativity, with the same capacity.
