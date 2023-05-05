# Fractional knapsack

The knapsack problem when items can be cut.

| | |
|---|---|
| Time | O(n log n), the sort |
| Space | O(n) |
| Greedy rule | highest value per unit weight |

## The idea

Identical to [0/1 knapsack](../../dynamic-programming/knapsack-01/) except
that a fraction of an item may be taken, for a proportional fraction of its
value. Sort by value per weight, take items whole while they fit, and fill the
last of the space with a fraction of the next one.

## Why greedy works here and not there

Both versions have optimal substructure. That is not what separates them.

The difference is whether the greedy choice can always be extended to an
optimal solution. Here it can: any space left over is filled by part of the
next item, so committing to the densest item costs nothing. In the 0/1 version
an item either fits or it does not, so taking the densest one can leave a gap
that no remaining item fills, and a different choice would have done better.
Weights 10, 20, 30 with values 60, 100, 120 and capacity 50 is the standard
demonstration: fractional gets 240, greedy on the 0/1 version gets 160, and
the 0/1 optimum is 220.

Both are in this repository, so the comparison can be run.

## What is worth noticing

One relaxation of the rules moves the problem from NP-complete to O(n log n),
and the algorithm from a dynamic programming table to a sort. The pair is the
sharpest available statement of what greedy algorithms actually need.

The fractional optimum is also an upper bound on the 0/1 optimum, since any 0/1
solution is a legal fractional one. Branch and bound solvers for 0/1 knapsack
use exactly this to prune, which is a good example of a relaxation being useful
precisely because it is easy.
