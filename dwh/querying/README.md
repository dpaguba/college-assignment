# Querying

| Topic | |
|---|---|
| [olap-operations](olap-operations/) | the four cube operations |
| [star-joins](star-joins/) | three plans, a thousandfold apart |
| [materialized-views](materialized-views/) | the lattice of aggregates |
| [view-selection](view-selection/) | choosing under a budget |

Part V of the lecture. The block is a chain of consequences: a cube of ten
dimensions has 1024 possible aggregates, so they cannot all be stored, so
queries have to be answered from the fact table, so the join has to avoid
reading it, so the indices of the next block exist.

The measured contrast: the naive star join reads a million rows and the
bitmap plan reads a thousand.
