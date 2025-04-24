# Bucket sort

Scatter into ranges, sort each range, concatenate.

| | |
|---|---|
| Best | O(n + k) |
| Average | O(n + k) |
| Worst | O(n²) |
| Memory | O(n + k) |
| Stable | yes |
| Family | non-comparison |

## The idea

The n log n lower bound is a statement about comparison sorts: any algorithm that
learns about the data only by asking "is a < b" needs at least log₂(n!) questions.
Every sort in this family sidesteps the bound by looking at the key itself instead
of comparing keys, so the proof simply does not apply to them.

Split the key range into equal intervals, drop each element into the interval it
belongs to, sort the intervals separately and join them.

Everything depends on an assumption about the data: that the keys are spread
roughly evenly. If they are, each bucket holds a handful of elements and the total
is linear. If they all land in one bucket, the cost is whatever the inner sort
costs, n² here. This is the sort that is fast because of what it assumes, not
because of what it does.

## How it runs

1. Find the key range and divide it into n intervals.
2. Place each element in the interval its key falls into.
3. Sort each bucket with insertion sort, which is fast on short lists.
4. Concatenate.

## When it is the right choice

Uniformly distributed numeric data, floating point in particular. It is also the shape of every parallel sort: buckets are independent.
