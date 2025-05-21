# Quicksort

Pick a pivot, put everything smaller on the left and larger on the right, recurse.

| | |
|---|---|
| Best | O(n log n) |
| Average | O(n log n) |
| Worst | O(n²) |
| Memory | O(log n) |
| Stable | no |
| Family | exchange |

## The idea

Hoare's algorithm, and the reason divide and conquer is taught at all. One
partition pass puts the pivot in its final position and guarantees that nothing on
the left is bigger than anything on the right. The two sides never interact again.

No merge step is needed, which is what makes it faster in practice than merge sort
despite the worse worst case: the work happens on the way down, not on the way
back up, and it happens in place.

The pivot choice is everything. A fixed pivot on sorted input splits off one
element at a time and the recursion becomes n deep. This implementation picks at
random, which turns the bad case from a property of the input into a matter of
luck.

## How it runs

1. Choose a pivot.
2. Partition: scan from both ends, swapping pairs that are on the wrong side.
3. Recurse into the smaller side, loop on the larger one. That keeps the stack at
   O(log n) even when the splits are uneven.

## When it is the right choice

The default in-memory sort when stability is not needed. Every practical variant, introsort and pdqsort, starts here and adds a guard against the worst case.
