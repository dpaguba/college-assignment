# Pigeonhole sort

One hole per key, drop each element in, read the holes in order.

| | |
|---|---|
| Best | O(n + r) |
| Average | O(n + r) |
| Worst | O(n + r) |
| Memory | O(r) |
| Stable | yes |
| Family | non-comparison |

## The idea

The n log n lower bound is a statement about comparison sorts: any algorithm that
learns about the data only by asking "is a < b" needs at least log₂(n!) questions.
Every sort in this family sidesteps the bound by looking at the key itself instead
of comparing keys, so the proof simply does not apply to them.

Counting sort's simpler cousin: instead of counting first and placing second, keep
a list per key and concatenate them at the end. Same complexity, more memory,
easier to read.

## How it runs

1. Allocate one list per key in the range.
2. Append each element to its key's list.
3. Concatenate the lists in key order.

## When it is the right choice

The same narrow situation as counting sort, when clarity matters more than the extra allocations.
