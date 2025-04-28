# Cocktail shaker sort

Bubble sort that alternates direction, so small values at the end stop crawling.

| | |
|---|---|
| Best | O(n) |
| Average | O(n²) |
| Worst | O(n²) |
| Memory | O(1) |
| Stable | yes |
| Family | exchange |

## The idea

Bubble sort is asymmetric. A large value at the front travels to the end in a
single pass, because each swap carries it one more step in the same pass. A small
value at the end moves left by exactly one position per pass, no matter how far
it has to go. Those slow ones are called turtles.

Sweeping right and then left gives the turtles the same treatment the large
values already got.

## How it runs

1. Sweep left to right swapping out-of-order neighbours. The largest value lands
   at the right end.
2. Sweep right to left doing the same. The smallest value lands at the left end.
3. Shrink the range from both sides and repeat until a full round makes no swaps.

## Worked example

```
[3, 4, 5, 1]   forward:  3,4 keep  4,5 keep  5,1 swap
[3, 4, 1, 5]   5 is final
[3, 4, 1, 5]   backward: 4,1 swap  3,1 swap
[1, 3, 4, 5]   1 is final, and the list happens to be sorted

Plain bubble sort needs three passes for the same input, because the 1 moves
left one position at a time.
```

## When it is the right choice

The same answer as bubble sort: not in production. It halves the constant on
inputs with a few displaced small values and changes nothing asymptotically.
