# Bubble sort

Walk the list, swap neighbours that are out of order, repeat until a pass makes no swaps.

| | |
|---|---|
| Best | O(n) |
| Average | O(n²) |
| Worst | O(n²) |
| Memory | O(1) |
| Stable | yes |
| Family | exchange |

## The idea

Two neighbours that are in the wrong order are a local defect, and swapping them
fixes it. Do that everywhere, repeatedly, and the list is sorted, because a list
with no local defects has no global ones either.

Each pass carries the largest remaining value all the way to the end, the way a
bubble rises, which is where the name comes from. After k passes the last k
positions are final, so the next pass can stop k earlier.

## How it runs

1. Compare positions 0 and 1, swap if the first is larger. Then 1 and 2, and so on.
2. At the end of the pass the largest element is in the last position. Shrink the
   range by one.
3. If a whole pass made no swaps, nothing is out of order: stop.

That early exit is the only reason the best case is linear. Without it every
input costs the same n² comparisons.

## Worked example

```
[5, 1, 4, 2]   compare 5,1 -> swap
[1, 5, 4, 2]   compare 5,4 -> swap
[1, 4, 5, 2]   compare 5,2 -> swap
[1, 4, 2, 5]   pass done, 5 is final

[1, 4, 2, 5]   compare 1,4 -> keep
[1, 4, 2, 5]   compare 4,2 -> swap
[1, 2, 4, 5]   pass done, 4 is final

[1, 2, 4, 5]   compare 1,2 -> keep, no swaps this pass -> stop
```

## When it is the right choice

Almost never in production. It is the sort you write on a whiteboard, and the one
worth knowing because every other exchange sort is described as a fix for one of
its faults: cocktail shaker fixes the asymmetry, comb sort fixes the one-step
movement, quicksort abandons neighbour swaps altogether.
