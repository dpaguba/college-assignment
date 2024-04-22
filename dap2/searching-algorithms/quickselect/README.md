# Quickselect

Quicksort that recurses into one side only.

| | |
|---|---|
| Average | O(n) |
| Worst | O(n²) |
| Memory | O(1) beyond the copy |
| Needs | nothing |
| Answers | what is the k-th smallest value |

## The idea

Quicksort partitions and then sorts both sides. If only the k-th element is wanted,
just one side can contain it, so the other is discarded unsorted. The recurrence
changes from T(n) = 2T(n/2) + n to T(n) = T(n/2) + n, and the sum collapses from
n log n to n.

Expected linear time, worst case n² for the same reason quicksort has one: a pivot
that keeps landing at an end. Random pivots make that a matter of luck rather than a
property of the input.

This implementation partitions three ways, into smaller, equal and larger, so a run
of duplicate keys cannot cause the quadratic behaviour a two-way split allows.

It is how a median is computed without sorting, and how the top k of a million
records are found without ordering the rest.

## How it runs

1. Pick a random pivot and partition into smaller, equal and larger.
2. If k falls in the equal block, that is the answer.
3. Otherwise loop on the side that contains k.

## When it is the right choice

Medians, percentiles, top-k queries. Anywhere the order of the other elements is irrelevant.
