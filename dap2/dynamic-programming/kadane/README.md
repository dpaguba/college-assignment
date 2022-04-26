# Kadane's algorithm

The best contiguous run, in one pass.

| | |
|---|---|
| Time | O(n) |
| Space | O(1) |
| Table shape | running value |

## The idea

Brute force is O(n²): every start against every end. Divide and conquer brings it
to O(n log n) by splitting and handling the runs that cross the middle, which is the
version the divide and conquer lecture uses.

Kadane asks a smaller question. For each position, what is the best run **ending
here**? There are only two candidates: this element alone, or this element added to
the best run ending one position back. One comparison, and the answer to the whole
problem is the best of those n answers.

## The recurrence

```
best_ending_here(i) = max(values[i], best_ending_here(i-1) + values[i])
```

## What is worth noticing

The reframing from "best run anywhere" to "best run ending here" is the move that
turns a search into a recurrence, and it reappears throughout this folder: the state
has to be something a single step can extend.

All-negative input is where naive versions break. Initialising the running total to
zero reports zero for an array with no empty run allowed, so the first element is
the correct starting point.
