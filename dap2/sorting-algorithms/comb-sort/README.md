# Comb sort

Bubble sort with a shrinking gap, which kills long-range disorder early.

| | |
|---|---|
| Best | O(n log n) |
| Average | O(n²) |
| Worst | O(n²) |
| Memory | O(1) |
| Stable | no |
| Family | exchange |

## The idea

Bubble sort's weakness is that an element moves one position per pass. Comb sort
compares elements that are a wide gap apart, so a value near the wrong end crosses
most of the list in a single swap. The gap shrinks by a factor of 1.3 each pass and
the final pass, with gap 1, is plain bubble sort on data that is nearly ordered.

The 1.3 is empirical: larger and the passes leave too much disorder, smaller and
you are back to bubble sort.

## How it runs

1. Start with gap = n.
2. Compare and swap every pair `gap` apart.
3. Divide the gap by 1.3, floor it, and repeat.
4. Once the gap is 1, keep passing until a pass makes no swaps.

## When it is the right choice

A one-line improvement to bubble sort when you want something better and refuse to write anything longer. Shellsort does the same thing more carefully.
