# Odd-even merge sort

Batcher's other network: the same depth as bitonic, with fewer comparators.

| | |
|---|---|
| Best | O(n log² n) |
| Average | O(n log² n) |
| Worst | O(n log² n) |
| Memory | O(1) |
| Stable | no |
| Family | network |

## The idea

The merge is the clever part. Given two sorted halves, sort the odd-indexed elements
together and the even-indexed ones together, and then one pass of neighbour
comparisons finishes the job.

That the last pass suffices is not obvious, and the proof is the zero-one principle
again: check it for all sequences of zeros and ones and it holds for everything.
This folder's test does that exhaustively up to width 16.

Same O(log² n) depth as bitonic sort with a lower comparator count, which is what
matters when the network is etched into hardware.

## How it runs

1. Sort both halves recursively.
2. Odd-even merge them: the odd subsequences together, the even ones together, then
   a single neighbour pass.
3. Pad to a power of two.

## When it is the right choice

Hardware sorting networks, and as the standard example in the theory of oblivious algorithms.
