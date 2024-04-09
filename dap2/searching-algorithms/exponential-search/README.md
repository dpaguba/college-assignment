# Exponential search

Double the bound until it passes the target, then binary search that range.

| | |
|---|---|
| Average | O(log i) |
| Worst | O(log n) |
| Memory | O(1) |
| Needs | a sorted array |
| Answers | where is this value |

## The idea

Also called doubling or galloping search. Check positions 1, 2, 4, 8, 16 until the
value there passes the target, then binary search between the last two bounds.

Finding the bound costs log(i) steps, where i is the answer's position, and the
binary search costs another log(i). So a target near the front is found in a handful
of comparisons no matter how long the array is, which binary search cannot promise
because it always starts in the middle.

Two consequences. It works on unbounded or streamed sorted input, where the length
is unknown. And galloping inside timsort is exactly this: when one run keeps winning
the merge, doubling finds how far it wins by far faster than stepping would.

## How it runs

1. Double an index until the value there exceeds the target or the array ends.
2. Binary search between the previous bound and this one.

## When it is the right choice

Unbounded or streaming sorted data, targets expected near the front, and as the galloping step inside adaptive merges.
