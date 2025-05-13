# Merge sort

Split in half, sort both halves, merge them.

| | |
|---|---|
| Best | O(n log n) |
| Average | O(n log n) |
| Worst | O(n log n) |
| Memory | O(n) |
| Stable | yes |
| Family | merge |

## The idea

The textbook divide and conquer. The recursion tree is log n levels deep and every
level touches each element once, so the cost is n log n on every input. There is no
bad case, which is what separates it from quicksort.

Stability comes from one character in the merge: taking from the left half on a
tie, `<=` rather than `<`, keeps equal elements in their original order.

The n extra slots are the price. That is why quicksort usually wins in memory, and
why merge sort wins as soon as the data does not fit in memory at all: sequential
reads and writes are exactly what disks and tapes are good at.

## How it runs

1. Split the list at the middle.
2. Sort each half recursively.
3. Merge: walk both halves with two indices, always taking the smaller head.

## When it is the right choice

Anywhere stability matters, anywhere the worst case matters, and all of external sorting. Timsort is merge sort with run detection.
