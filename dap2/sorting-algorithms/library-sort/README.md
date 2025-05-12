# Library sort

Insertion sort that leaves gaps, so an insertion shifts a few elements instead of thousands.

| | |
|---|---|
| Best | O(n log n) |
| Average | O(n log n) |
| Worst | O(n²) |
| Memory | O(n) |
| Stable | no |
| Family | insertion |

## The idea

Also called gapped insertion sort. A librarian shelving a new book does not slide
the entire shelf along: the shelves have gaps.

The array is kept at roughly twice the needed size with empty slots spread between
the elements, so an insertion shifts only until the nearest gap. Binary search finds
the destination, and when a region fills up the whole array is rebalanced and the
gaps redistributed. That gives n log n with high probability, while keeping the
simplicity of insertion sort.

## How it runs

1. Binary search the occupied slots for the insertion point.
2. Walk right to the nearest gap and shift the handful of elements in between.
3. When the array gets too full, respread everything evenly and continue.

## When it is the right choice

Rarely used directly. It matters as the sorting cousin of the packed memory array, which is the structure behind cache-oblivious B-trees.
