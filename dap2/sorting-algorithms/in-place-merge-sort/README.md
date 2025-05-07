# In-place merge sort

The same recursion, merging by rotating blocks instead of copying.

| | |
|---|---|
| Best | O(n) |
| Average | O(n log² n) |
| Worst | O(n log² n) |
| Memory | O(log n) |
| Stable | yes |
| Family | merge |

## The idea

Ordinary merge sort needs n spare slots for the merge. This version merges two
adjacent sorted runs without them: take the median of the longer run, binary search
for its place in the other, and rotate the blocks between the two cut points. Now
the problem has split into two independent smaller merges.

Nothing is free. The rotations turn a linear merge into n log n and the whole sort
into n log² n. This is the trade when memory, not time, is the scarce resource.

## How it runs

1. Sort each half recursively.
2. To merge, pick the median of the longer run and find its position in the other.
3. Rotate the middle blocks past each other so the two halves of the problem no
   longer overlap.
4. Recurse into both.

## When it is the right choice

Embedded and kernel code where allocating n slots is not allowed but stability is required.
