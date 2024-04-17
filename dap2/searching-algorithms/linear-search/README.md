# Linear search

Look at every element until the target turns up.

| | |
|---|---|
| Average | O(n) |
| Worst | O(n) |
| Memory | O(1) |
| Needs | nothing |
| Answers | where is this value |

## The idea

The only search that asks nothing of the data: no order, no index, no structure.

That is not a weakness, it is the argument for it. Everything faster on this list
requires a sorted array, and sorting costs n log n. For one lookup in unsorted data
linear search is the optimal algorithm, not the naive one. It only loses when the
same array is searched many times and the sort can be amortised over all of them.

It is also the only search here that works on something you can walk but not index:
a stream, a linked list, a generator.

## How it runs

Walk from the start, compare each element, return the first index that matches, or -1.

## When it is the right choice

Unsorted data, a single lookup, tiny arrays where the constant beats the logarithm, and anything that is not randomly accessible.
