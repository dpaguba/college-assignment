# Interval partitioning

Use the fewest rooms so that no two intervals share a room and overlap.

| | |
|---|---|
| Time | O(n log n) |
| Space | O(n) |
| Greedy rule | earliest start, reuse the room that frees up soonest |

## The idea

The same intervals as in [interval-scheduling](../interval-scheduling/), the
opposite question: instead of dropping requests to fit one room, keep every
request and ask how few rooms suffice.

Sort by start time. For each interval, if some room is already free, put it
there; otherwise open a new one. A min-heap keyed on the finishing time of
each room makes "is any room free" a single comparison.

## The lower bound

The **depth** is the largest number of intervals that are live at one moment.
No schedule can use fewer rooms than the depth, since at that moment every one
of those intervals needs a room of its own. `maximum_overlap()` computes it by
sweeping the start and end events.

## The proof

Greedy opens a new room only when every existing room is busy. Suppose it
opens room number d. At that instant the interval being placed overlaps with
one interval in each of the d − 1 other rooms, so d intervals are live at once
and the depth is at least d.

So greedy uses at most depth rooms and every schedule uses at least depth
rooms. The bound is met exactly, which is stronger than most greedy results:
this is not "greedy happens to be optimal", it is "greedy achieves a bound
that is obviously unachievable in general".

## What is worth noticing

The same algorithm is interval graph colouring. Interval graphs are perfect,
meaning the chromatic number equals the largest clique, and the two paragraphs
above are exactly that fact for this special case. Colouring an arbitrary graph
with the fewest colours is NP-hard, and this sorting-based algorithm solves it
for intervals because their structure is one-dimensional.
