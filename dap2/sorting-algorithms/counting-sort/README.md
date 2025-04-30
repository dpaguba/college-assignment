# Counting sort

Count how many of each key there are, then lay them out in one pass.

| | |
|---|---|
| Best | O(n + r) |
| Average | O(n + r) |
| Worst | O(n + r) |
| Memory | O(n + r) |
| Stable | yes |
| Family | non-comparison |

## The idea

The n log n lower bound is a statement about comparison sorts: any algorithm that
learns about the data only by asking "is a < b" needs at least log₂(n!) questions.
Every sort in this family sidesteps the bound by looking at the key itself instead
of comparing keys, so the proof simply does not apply to them.

Here the count of each key says how many slots it occupies, and the running total
of the counts says where its block starts. Two passes and the array is built.

The cost is a counter per possible key. Sorting three numbers that happen to be a
million apart allocates a million counters, which is why this is only sensible when
the key range is comparable to the number of elements.

## How it runs

1. Count occurrences of each key.
2. Turn the counts into starting positions with a running total.
3. Walk the input placing each element at its key's next free position.

## When it is the right choice

Small dense key ranges: ages, grades, bytes, pixel values. Also the inner pass of radix sort, which is where it does most of its real work.
