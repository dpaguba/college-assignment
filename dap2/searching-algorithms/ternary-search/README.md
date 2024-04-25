# Ternary search

Two cuts per step, to find a peak rather than a value.

| | |
|---|---|
| Average | O(log₃ n) |
| Worst | O(log₃ n) |
| Memory | O(1) |
| Needs | a unimodal sequence |
| Answers | where is the maximum |

## The idea

This one answers a different question from everything else here. Binary search asks
where a value is; ternary search asks where the largest value is, and it requires
the sequence to rise and then fall, with no plateau at the top.

Cut the range at two points a third apart. If the left probe is smaller than the
right one, the peak cannot lie left of the left probe, so that third is discarded,
and symmetrically. Each step throws away a third at the cost of two comparisons.

It generalises straight to continuous functions, and that is its real home: finding
the minimum of a convex cost function when no derivative is available. Golden
section search is the same idea with a better constant.

## How it runs

1. Probe at one third and two thirds of the range.
2. Discard the third that cannot contain the peak.
3. When three or fewer candidates remain, compare them directly.

## When it is the right choice

Optimisation of unimodal functions, not lookup. For a sorted array, binary search is strictly better.
