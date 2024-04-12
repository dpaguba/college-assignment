# Interpolation search

Guess the position from the value, the way a phone book is used.

| | |
|---|---|
| Average | O(log log n) |
| Worst | O(n) |
| Memory | O(1) |
| Needs | sorted and evenly distributed keys |
| Answers | where is this value |

## The idea

Nobody opens a phone book in the middle to find Aaronson. Binary search does exactly
that, because it uses only the order of the keys and never their values.

Interpolation search uses the values: assuming the data rises evenly, it estimates
the target's position by linear interpolation between the ends of the range. On
uniform keys the estimate lands close enough that the remaining range shrinks doubly
exponentially, giving O(log log n). A million elements take about four probes rather
than twenty.

The uniformity assumption is load bearing. On keys like 1, 2, 3, ..., 1000, 10⁹ the
estimate lands at the wrong end every time and the search degrades to O(n), worse
than binary search on the same data. Production implementations detect the
degeneration and fall back.

## How it runs

1. Estimate the position from the target's value relative to the range's endpoints.
2. Probe there; narrow the range to one side; repeat.

## When it is the right choice

Large arrays of evenly spread numeric keys: timestamps, sequential ids, sensor readings.
