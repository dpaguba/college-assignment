# Insertion sort

Take the next element and slide it back into the sorted part.

| | |
|---|---|
| Best | O(n) |
| Average | O(n²) |
| Worst | O(n²) |
| Memory | O(1) |
| Stable | yes |
| Family | insertion |

## The idea

How people sort a hand of cards. The left part of the array is always sorted; each
step takes the first unsorted element and moves it left past everything larger.

Two properties make it matter far beyond its n². It is adaptive: on nearly sorted
input the inner loop stops on the first comparison, so the cost is linear. And it
is stable, because the comparison is strict: an element never moves past an equal
one.

Both properties are why insertion sort is inside timsort, introsort, pdqsort,
bucket sort and shellsort. It is the sort that finishes what the others start.

## How it runs

1. Assume position 0 is sorted.
2. Take position i, walk left while the neighbour is strictly larger, shifting it right.
3. Drop the value into the hole.

## When it is the right choice

Small arrays, up to roughly 16 to 32 elements, and nearly sorted data. Every serious sort switches to it at the bottom of the recursion.
