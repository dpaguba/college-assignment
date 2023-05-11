# Interval scheduling

Pick the largest set of intervals that do not overlap.

| | |
|---|---|
| Time | O(n log n), all of it the sort |
| Space | O(n) |
| Greedy rule | earliest finishing time |

## The idea

One room, a list of requests with a start and an end, and the goal is to accept
as many as possible. Note what is not being maximised: not the total time
booked, not the value of the requests, just the count.

The rule is to repeatedly take the interval that **finishes earliest** among
those still compatible with what is already accepted. Finishing early leaves
the most room for everything after it.

## Why the obvious rules fail

Both of these are implemented in `interval_scheduling.py` so the failures can
be run rather than taken on trust.

**Earliest start.** `[(0, 10), (1, 2), (3, 4)]`. The long interval starts first
and blocks both short ones: one accepted instead of two.

**Shortest interval.** `[(0, 5), (4, 6), (5, 10)]`. The short middle interval
overlaps both of its neighbours and blocks them: one instead of two.

## The proof

A **stays ahead** argument. Let the greedy picks be g₁, g₂, … and some optimal
solution be o₁, o₂, … , both in order of finishing time. By induction, gᵢ
finishes no later than oᵢ: it is true for the first pick because greedy takes
the earliest finisher of all, and if it holds for i then gᵢ leaves at least as
much room as oᵢ, so the interval greedy takes next finishes no later than
oᵢ₊₁.

If the optimum had more intervals than greedy, there would be an interval
oₖ₊₁ compatible with o₁…oₖ, and since gₖ finishes no later than oₖ, it would
also be compatible with g₁…gₖ. Greedy would have taken it. It stopped, so
there is no such interval, and the two solutions have the same size.

## What is worth noticing

Weighted interval scheduling, where each interval has a value and the goal is
maximum total value, breaks every greedy rule and needs dynamic programming.
The unweighted version is the boundary case: as soon as intervals stop being
interchangeable, sorting is not enough.
