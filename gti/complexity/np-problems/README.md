# The NP problems

Nine problems, each with a **verifier** and a **brute force solver**, kept
apart on purpose. That separation is the definition of NP: a certificate can be
checked quickly even when finding one is hard.

| Problem | Certificate | Verifier cost |
|---|---|---|
| SAT | an assignment | linear in the formula |
| 3SAT | an assignment | linear |
| CLIQUE | k vertices | quadratic in k |
| VERTEX COVER | k vertices | linear in the edges |
| INDEPENDENT SET | k vertices | quadratic in k |
| HAMILTONIAN CYCLE | an order of the vertices | linear |
| SUBSET SUM | indices | linear |
| KNAPSACK | indices | linear |
| TSP | a tour | linear |

## Three problems, one structure

A set is a clique in G exactly when it is an independent set in the complement,
and exactly when its complement is a vertex cover. That is why the reductions
between them in [np-reductions](../np-reductions/) are three lines each, and
why an exercise that asks for one usually accepts the other.

## Certificates are indices, not values

`subset_sum_verify` takes indices, because a list may contain the same number
twice and a set of values would lose that. Small detail, and the kind that
makes a verifier subtly wrong.

## Two solvers for SAT

`satisfiable_solve` tries all 2^n assignments and exists to define the problem.
`satisfiable_dpll` is unit propagation, pure literals and backtracking, and it
is here because the [Cook-Levin](../cook-levin/) encoding produces formulas with
hundreds of variables where enumeration is hopeless.

Both were checked against each other on 300 random formulas, with every model
validated by the verifier rather than trusted.
