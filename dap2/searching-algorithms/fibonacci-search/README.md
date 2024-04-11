# Fibonacci search

Binary search that only ever adds and subtracts.

| | |
|---|---|
| Average | O(log n) |
| Worst | O(log n) |
| Memory | O(1) |
| Needs | a sorted array |
| Answers | where is this value |

## The idea

Split the range at a Fibonacci number instead of at the middle. Because
F(k) = F(k-1) + F(k-2), moving into either sub-range is a subtraction and the next
split point is already in the table. No division, no midpoint computation.

That mattered when division cost tens of cycles and addition cost one, and it still
matters on microcontrollers without a divider. The split sits at the golden ratio
rather than the middle, so it makes slightly more comparisons than binary search:
that is the price of the cheaper arithmetic.

The probes also step through memory in smaller increments than binary search's
halving, which is friendlier to a cache or a tape.

## How it runs

1. Find the smallest Fibonacci number not smaller than the array length.
2. Probe at the offset given by the smaller of the two preceding Fibonacci numbers.
3. Shift the pair of Fibonacci numbers down and repeat.

## When it is the right choice

Hardware without a divider, and sequential media where locality matters more than comparison count.
