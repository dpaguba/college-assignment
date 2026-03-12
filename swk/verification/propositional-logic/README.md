# Propositional logic

Formulas, normal forms, and the one question everything reduces to.

The lecture states three notions in one place, and they are the same notion:

| | holds when |
|---|---|
| satisfiable | some assignment makes the formula true |
| contradictory | no assignment makes both formulas true |
| entailment, `phi \|= psi` | no assignment makes `phi and not psi` true |

Entailment is the one that matters. Bounded model checking, inductive
invariants and Hoare proofs are all entailment checks, and each is answered by
asking a solver about the **negation**. A model of the negation is a
counterexample, which is usually more useful than the yes or no.

## Two ways to reach CNF

`to_cnf` distributes `or` over `and`. Correct, and exponential: an `or` of two
conjunctions multiplies their clause counts. On the eight-way example in this
folder it produces 256 clauses.

`to_tseitin` names every subformula with a fresh atom and adds clauses forcing
the name to agree with what it names. The result is not equivalent to the
original, it is **equisatisfiable**, which is all a solver needs, and it is
linear in the size of the formula: 34 clauses for the same example.

Every real solver front end does the Tseitin transformation. Without it, the
million-clause instances that industrial verification produces could not be
written down at all.

## The brute force checker

`brute_force_satisfiable` tries all 2^n assignments. It exists as the
reference the real solvers are checked against, and it is exactly what
[DPLL](../dpll/) and [CDCL](../cdcl/) are built to avoid.
