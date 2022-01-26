# Closest pair of points

The two nearest points among n, in O(n log n).

| | |
|---|---|
| Time | O(n log n) |
| Recurrence | `T(n) = 2T(n/2) + O(n)` |
| Master theorem | case 2, every level costs the same |

## The idea

Checking every pair costs O(n²). Sort by x, split at the median, solve both halves,
and let d be the better answer. A closer pair must have one point in each half and
both within d of the dividing line, so only that strip needs checking.

## What is worth noticing

**The strip can still hold every point**, so scanning it naively brings the n² back.
The saving comes from geometry: within the strip, sorted by y, a point can only be
closer than d to the next seven. An eighth would force two points on the same side
to be closer than d to each other, contradicting d being the best within a half.

That constant, seven, is what makes the merge linear. It is the clearest case in the
course of a bound that comes from the shape of the problem rather than from
bookkeeping.
