# Sentinel linear search

Put the target at the end so the loop only needs one test per step.

| | |
|---|---|
| Average | O(n) |
| Worst | O(n) |
| Memory | O(n) for the copy |
| Needs | a writable end slot |
| Answers | where is this value |

## The idea

Plain linear search checks two things per iteration: have I found it, and have I run
off the end. Writing the target into the last slot guarantees the first check
eventually succeeds, so the bounds test can leave the loop entirely and appear once
afterwards to ask whether the match was the real one or the sentinel.

Half the comparisons per step, and no change in complexity whatsoever. It is the
clearest example of a constant-factor optimisation: exactly what big-O is defined to
ignore, and exactly what a profiler will show you.

This implementation copies the array first, because a search has no business
modifying what it was handed. In C, where the technique comes from, it writes into
the caller's buffer and restores it afterwards.

## How it runs

1. Remember the last element and overwrite it with the target.
2. Walk forward with no bounds check until a match is found.
3. If the match is before the last slot it is real; otherwise check the remembered
   value.

## When it is the right choice

Historical, and instructive. Modern compilers and branch predictors make the saving hard to measure.
