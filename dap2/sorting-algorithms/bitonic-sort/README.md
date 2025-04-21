# Bitonic sort

A sorting network: which elements get compared is fixed before the data is seen.

| | |
|---|---|
| Best | O(n log² n) |
| Average | O(n log² n) |
| Worst | O(n log² n) |
| Memory | O(1) |
| Stable | no |
| Family | network |

## The idea

Ken Batcher's network. A bitonic sequence rises and then falls. The network builds
one out of the input, then splits it into halves that are each bitonic again, and
repeats until everything is ordered.

What makes it a network rather than an algorithm: the comparisons depend only on
position, never on a value. Every comparison within a stage is independent, so
hardware or a GPU performs the whole stage in one step. The depth is log²(n)
stages, and that is the number that matters there, not the O(n log² n) comparisons
a single processor would perform.

The correctness argument is the zero-one principle: a network that sorts every
sequence of zeros and ones sorts every sequence at all. The test in this folder
checks exactly that, for every input of width 4, 8 and 16.

## How it runs

1. Recursively sort the first half ascending and the second half descending. The
   concatenation is bitonic.
2. Bitonic merge: compare each element with the one half a length away, then recurse
   into both halves.
3. Pad to a power of two, since the network's shape requires it.

## When it is the right choice

GPUs and FPGAs, where the fixed comparison schedule is the whole advantage. Never on a single core.
