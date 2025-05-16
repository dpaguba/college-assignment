# Patience sort

Deal into piles like the card game, then merge the piles.

| | |
|---|---|
| Best | O(n) |
| Average | O(n log n) |
| Worst | O(n log n) |
| Memory | O(n) |
| Stable | no |
| Family | insertion |

## The idea

Deal each card onto the leftmost pile whose top card is not smaller, and start a new
pile when none will take it. Every pile ends up decreasing from bottom to top, so
merging the piles with a heap produces sorted output.

The sorting is the side effect. The number of piles is exactly the length of the
longest increasing subsequence of the input, and that is what the algorithm is
actually used for. `longest_increasing_subsequence_length` in this folder is the
same dealing loop with the merge thrown away.

## How it runs

1. For each value, binary search the pile tops for the first one that is at least
   as large, and place it there. Otherwise open a new pile.
2. Merge the piles with a min-heap over their top cards.

## When it is the right choice

Computing a longest increasing subsequence in n log n, which is its real job. As a sort it is merge sort with a worse constant.
