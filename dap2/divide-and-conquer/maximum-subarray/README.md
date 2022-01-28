# Maximum subarray, divide and conquer

Left, right, or crossing the middle.

| | |
|---|---|
| Time | O(n log n) |
| Recurrence | `T(n) = 2T(n/2) + O(n)` |
| Master theorem | case 2, every level costs the same |

## The idea

Split the array in half. The best run lies entirely in the left half, entirely in
the right, or crosses the middle. The first two are the same problem on smaller
input; the third is the only new work, and it is found greedily in linear time by
walking outwards from the centre.

## What is worth noticing

Kadane, in the dynamic programming folder, answers the same question in O(n), and
the two are tested against each other.

This version is kept because the reasoning matters more than the result. "Left,
right, or crossing" is the template for every divide and conquer argument, and this
is the smallest problem where the crossing case is not trivial.
