# Greedy algorithms

Five problems, one folder each, in plain Python with no dependencies. Every
folder holds the implementation and a README explaining the rule, the proof
that it is correct, and where the same rule stops working.

## What makes an algorithm greedy

Build the answer one commitment at a time, always taking what looks best right
now, and never reconsider. The code is nearly always trivial, usually a sort
followed by one pass. All the difficulty is in the proof.

Being greedy is easy. Being greedy and correct is not, and there is no way to
tell the two apart by reading the code.

## The problems

| Problem | Rule | Time |
|---|---|---|
| [interval-scheduling](interval-scheduling/) | earliest finishing time | O(n log n) |
| [interval-partitioning](interval-partitioning/) | earliest start, reuse the soonest-free room | O(n log n) |
| [minimising-lateness](minimising-lateness/) | earliest deadline | O(n log n) |
| [fractional-knapsack](fractional-knapsack/) | highest value per weight | O(n log n) |
| [huffman-coding](huffman-coding/) | merge the two least frequent | O(n log n) |

Every one is O(n log n) and every one is dominated by a sort or a heap. That
is the shape of the whole family.

## The two proof techniques

**Stays ahead.** Show that after each step the greedy partial solution is at
least as good as any other partial solution of the same size, then conclude it
cannot be overtaken. Used in interval scheduling.

**Exchange.** Take any optimal solution and transform it into the greedy one by
swaps that never make it worse, then conclude greedy is optimal too. Used in
minimising lateness, the fractional knapsack, and Huffman.

Interval partitioning uses a third and rarer form: prove a lower bound that no
solution can beat, then show greedy meets it exactly.

## Where greedy fails

Three of the five folders implement a rule that is wrong on purpose, with the
counterexample, because seeing the failure is the only reliable way to learn
which rule is which.

- Interval scheduling by earliest start, or by shortest interval. Both lose.
- Minimising lateness by shortest job. Loses.
- The 0/1 knapsack by value density. Loses, and it is in the
  [dynamic programming](../dynamic-programming/knapsack-01/) folder for
  exactly that comparison.

The pattern behind all three: a greedy choice is safe only when it can still
be extended to an optimal solution. Optimal substructure is not enough, which
is why [dynamic programming](../dynamic-programming/) exists.

## Related folders

Greedy choices also appear inside larger algorithms elsewhere in this module.
[Dijkstra](../graph-algorithms/dijkstra/) settles the nearest unsettled vertex,
[Prim](../graph-algorithms/prim/) and [Kruskal](../graph-algorithms/kruskal/)
add the cheapest safe edge. Their correctness rests on the cut property, which
is the same kind of exchange argument as the ones above.
