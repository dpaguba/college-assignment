# Dynamic programming

Thirteen problems, one folder each, in plain Python with no dependencies. Every
folder holds the implementation and a README explaining the idea, the
recurrence, and what is worth noticing about it.

## When it applies

Two properties, both required.

**Optimal substructure.** An optimal solution is built from optimal solutions
to subproblems. Without it, solving the parts well says nothing about the
whole.

**Overlapping subproblems.** The same subproblems recur, so there are few of
them. Without overlap there is nothing to cache, and divide and conquer is the
better fit: merge sort never sees the same subarray twice, which is exactly
why it is not dynamic programming.

## The four shapes

Recognising the shape is what makes a new problem tractable, and there are
only a few.

**Linear.** One index, each state built from a constant number of earlier ones.

| Problem | Time | Space |
|---|---|---|
| [fibonacci](fibonacci/) | O(n) | O(1) |
| [kadane](kadane/) | O(n) | O(1) |
| [maximum-difference](maximum-difference/) | O(n) | O(1) |
| [rod-cutting](rod-cutting/) | O(n²) | O(n) |
| [coin-change](coin-change/) | O(n·amount) | O(amount) |
| [longest-increasing-subsequence](longest-increasing-subsequence/) | O(n log n) | O(n) |

**Capacity.** Items against a budget.

| Problem | Time | Space |
|---|---|---|
| [knapsack-01](knapsack-01/) | O(n·capacity) | O(capacity) rolling |
| [unbounded-knapsack](unbounded-knapsack/) | O(n·capacity) | O(capacity) |
| [subset-sum-partition](subset-sum-partition/) | O(n·target) | O(target) |

**Two sequences.** A grid, each cell comparing one element from each.

| Problem | Time | Space |
|---|---|---|
| [longest-common-subsequence](longest-common-subsequence/) | O(n·m) | O(min(n,m)) rolling |
| [edit-distance](edit-distance/) | O(n·m) | O(n·m) |

**Interval.** A range split at every possible point.

| Problem | Time | Space |
|---|---|---|
| [matrix-chain-multiplication](matrix-chain-multiplication/) | O(n³) | O(n²) |

**Over subsets.** The state is a set, not an index.

| Problem | Time | Space |
|---|---|---|
| [held-karp](held-karp/) | O(n²·2ⁿ) | O(n·2ⁿ) |

## Three things this folder is really about

**The gap between calls and distinct answers.** Naive Fibonacci makes 2,692,537
calls to compute 31 numbers. Everything else here is that observation applied
to a harder problem.

**Pseudo-polynomial is not polynomial.** Knapsack and subset sum both run in
time proportional to a number in the input, and a number needs only its
logarithm in bits to write down. Both problems are NP-complete and these
algorithms do not contradict that. It is the distinction most people miss.

**The loop direction is part of the specification.** Walking capacities
downwards gives the 0/1 knapsack, upwards gives the unbounded one. Looping
coins outside counts combinations, inside counts permutations. The recurrence
says nothing about either; the code is where the choice is made, silently.

## How this was built

Test first. Each problem got a test file before it had an implementation, run
to watch it fail for the right reason, then the code, then the run again.

Where an exhaustive answer was affordable, the tests check against it rather
than against a hand-written expectation: knapsack against every subset,
subset sum against every combination, Kadane against every subarray, Held-Karp
against every permutation, matrix chain against every bracketing. Where two
methods exist, they check each other: the two LIS versions, the two knapsack
versions, the rolling and full LCS.

Edit distance is checked against properties rather than answers, symmetry and
the triangle inequality on random strings, because those are what make it a
metric rather than a score. That test caught a genuine mistake in its own
premise: the edits come out in descending position order and have to be
applied that way round, and applying them the other way produces a plausible
wrong string.

The tests were removed once all 60 passed, so what remains is the library and
the explanations.
