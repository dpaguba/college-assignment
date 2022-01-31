# Divide and conquer

Nine algorithms, one folder each, in plain Python with no dependencies. The
sorting folder holds the other half of this topic: merge sort and quicksort
are the canonical examples and live there.

Every one of these splits a problem into smaller copies of itself, solves
them, and combines the answers. What separates them is where the work goes.

| Algorithm | Recurrence | Result | Case |
|---|---|---|---|
| [karatsuba](karatsuba/) | T(n) = 3T(n/2) + O(n) | O(n^1.585) | leaves dominate |
| [strassen](strassen/) | T(n) = 7T(n/2) + O(n²) | O(n^2.807) | leaves dominate |
| [closest-pair-of-points](closest-pair-of-points/) | T(n) = 2T(n/2) + O(n) | O(n log n) | balanced |
| [maximum-subarray](maximum-subarray/) | T(n) = 2T(n/2) + O(n) | O(n log n) | balanced |
| [counting-inversions](counting-inversions/) | T(n) = 2T(n/2) + O(n) | O(n log n) | balanced |
| [binary-exponentiation](binary-exponentiation/) | T(n) = T(n/2) + O(1) | O(log n) | balanced |
| [convex-hull](convex-hull/) | sort plus a linear sweep | O(n log n) | not recursive |
| [binary-addition](binary-addition/) | one pass, no recursion | Θ(n) | the O(n) term itself |
| [master-theorem](master-theorem/) | reads all of the above | | |

## The one idea

Splitting is never the clever part. Eight block products give n³, which is
exactly what the definition costs, and two halves plus a linear merge give
n log n whether the problem is sorting, counting inversions or finding the
closest pair.

**What changes the answer is reducing the number of subproblems.** Karatsuba
takes four multiplications to three, Strassen takes eight to seven, and both
times the exponent falls. Everything else in this folder is an application of
the same recurrence at a fixed number of subproblems.

The [master-theorem](master-theorem/) folder holds a solver for exactly that
comparison, so the claims in each README can be checked rather than recalled.

## Divide and conquer against dynamic programming

Both break a problem into subproblems, and they part on one question: **do the
subproblems overlap?**

Merge sort never sees the same subarray twice, so there is nothing to cache
and the recursion is the algorithm. Fibonacci sees the same value
exponentially often, so caching is the algorithm. When the subproblems are
disjoint, divide and conquer; when they repeat, dynamic programming.

The maximum subarray problem is here in its divide and conquer form and in the
dynamic programming folder as Kadane, and the two are tested against each
other. Reading them side by side is the clearest way to see the difference.

## How this was built

Test first. Each algorithm got a test file before it had an implementation,
run to watch it fail for the right reason, then the code, then the run again.

Everything here computes something with an obvious slow answer, so the tests
check against it: Karatsuba against `*`, Strassen against three nested loops,
closest pair against every pair, inversions against every pair, the divide and
conquer maximum subarray against both brute force and Kadane, and both convex
hull methods against each other.

Two tests check the thing that actually matters rather than the answer:
Karatsuba is asserted to make three recursive products and Strassen seven,
because that count, not the result, is what the algorithms exist for.

The tests were removed once all 42 passed, so what remains is the library and
the explanations.
