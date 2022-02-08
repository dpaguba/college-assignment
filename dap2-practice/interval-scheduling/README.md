# Interval scheduling

The largest set of non-overlapping intervals. Practical sheet 6, task 6.1.

```
java IntervalSchedulingDemo
Auswahl: [[1,4], [5,7], [8,11], [12,16]]
2000 zufaellige Instanzen: greedy trifft jedes Mal das Optimum.
```

`Interval` and `IntervalScheduler` are the submission; the demo class exists
only so the result can be checked, since the sheet asks for both classes
without a main method.

## The rule

Repeatedly take the interval that finishes earliest among those still
compatible. O(n log n), all of it the sort, and the input arrives unsorted,
which is why the sort lives inside `run`.

Finishing early is the right thing to be greedy about, because it leaves the
most room for everything after it.

## Why the ordering lives in `Interval`

The algorithm is correct precisely because intervals are processed by
increasing end point, so the comparison belongs to the data type the algorithm
consumes rather than to a comparator passed in at the call site.
`compareTo` uses `Integer.compare` and not subtraction, which would overflow
for end points far apart.

## The proof

Stays ahead. Compare the greedy picks g₁, g₂, … with those of any optimal
solution o₁, o₂, …, both by finishing time. By induction gᵢ finishes no later
than oᵢ, so if the optimum had more intervals, the next one would still be
compatible with the greedy prefix and greedy would have taken it instead of
stopping.

## Where the obvious rules fail

Earliest start loses on [(0,10), (1,2), (3,4)] and shortest duration loses on
[(0,5), (4,6), (5,10)]; both accept one interval where two fit. Both
counterexamples are implemented in the
[dap2 greedy library](../../dap2/greedy-algorithms/interval-scheduling/).

## Verification

The lecture example, plus 2000 random instances checked against brute force
over all subsets. Greedy matched the optimum every time.
