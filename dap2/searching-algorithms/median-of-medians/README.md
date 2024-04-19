# Median of medians

Quickselect with a pivot chosen well enough to guarantee linear time.

| | |
|---|---|
| Average | O(n) |
| Worst | O(n) |
| Memory | O(n) |
| Needs | nothing |
| Answers | what is the k-th smallest value |

## The idea

Quickselect is linear on average and quadratic when the pivots are unlucky. Blum,
Floyd, Pratt, Rivest and Tarjan removed the luck in 1973.

Split the input into groups of five, take each group's median, and recursively
select the median of those medians. That pivot is guaranteed to be larger than at
least 30 percent of the elements and smaller than at least 30 percent, so every
level discards a constant fraction whatever the input. The recurrence
T(n) = T(n/5) + T(7n/10) + O(n) sums to O(n) precisely because 1/5 + 7/10 < 1.

Groups of five are not arbitrary: three is too small for the guarantee to hold, and
seven costs more per level than it saves.

The constant is large enough that plain quickselect wins in practice, so this is
the algorithm you cite rather than the one you run. Introselect uses quickselect and
falls back to this when the pivots go bad, exactly as introsort falls back to
heapsort.

## How it runs

1. Break the input into groups of five and take each group's median.
2. Recursively select the median of those medians as the pivot.
3. Partition and recurse into the side holding k.

## When it is the right choice

Proving a linear worst-case bound, and as the fallback inside introselect. Rarely the fastest choice on real data.
