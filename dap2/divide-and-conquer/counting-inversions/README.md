# Counting inversions

How far a sequence is from sorted, counted during a merge sort.

| | |
|---|---|
| Time | O(n log n) |
| Recurrence | `T(n) = 2T(n/2) + O(n)` |
| Master theorem | case 2, every level costs the same |

## The idea

An inversion is a pair i < j with values[i] > values[j]. The count is zero for
sorted input and n(n-1)/2 for reversed, and it is exactly the number of swaps
insertion sort performs, which is why insertion sort is linear on nearly sorted data.

Counting them directly is O(n²). **Merge sort already knows.** When an element is
taken from the right half while k elements remain on the left, that element is
smaller than all k of them, so k inversions are counted in one step.

## What is worth noticing

Counting costs nothing on top of the sort, so the whole thing is O(n log n). This is
the standard example of a divide and conquer algorithm that computes something other
than what it appears to: the sorting is a by-product and the count is the answer.

Listing the pairs is optional, because there can be n²/2 of them and asking for the
list throws away the reason the algorithm is fast.
