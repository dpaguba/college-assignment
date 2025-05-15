# Odd-even sort

Compare fixed pairs in two alternating phases, so a whole phase can run at once.

| | |
|---|---|
| Best | O(n) |
| Average | O(n²) |
| Worst | O(n²) |
| Memory | O(1) |
| Stable | yes |
| Family | exchange |

## The idea

Also called brick sort. One phase compares the pairs (0,1), (2,3), (4,5) and so on;
the next compares (1,2), (3,4), (5,6). No two comparisons in a phase share an
element, which means nothing in a phase depends on anything else in it.

That independence is the whole point. On a processor with n/2 comparators the phase
takes one step, and the sort finishes in n phases rather than n² comparisons. On a
single core it is bubble sort with extra bookkeeping.

## How it runs

1. Odd phase: compare and swap every pair starting at an odd index.
2. Even phase: the same starting at an even index.
3. Repeat until a full round changes nothing.

## When it is the right choice

Parallel hardware and systolic arrays. On one core, never.
