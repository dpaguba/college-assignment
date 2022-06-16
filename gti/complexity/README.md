# Complexity

Four modules for the fourth block of GTI: lectures 17 to 20, exercise sheet 12.

| Folder | What it does |
|---|---|
| [complexity-classes](complexity-classes/) | P, NP, verifiers, decision against optimisation |
| [np-problems](np-problems/) | nine problems, each with a verifier and a search |
| [np-reductions](np-reductions/) | the chain from SAT, with certificate transport |
| [cook-levin](cook-levin/) | a computation encoded as a formula |

## The shape of the block

The third block asked what can be computed **at all**. This one asks what can
be computed **quickly**, and the answer has the same structure: one hard
problem, and then everything else by reduction.

```
Cook-Levin: every NP problem  ->  SAT
then:       SAT -> 3SAT -> CLIQUE -> VERTEX COVER
                        -> INDEPENDENT SET
            HAMILTON -> TSP
```

## Everything here runs

The reductions are executable and were checked on random instances in both
directions: the yes-instances agree, and a certificate for the target maps back
to a certificate the source verifier accepts.

The Cook-Levin encoding is executable too, which is unusual for that theorem:
the formula for a nine-state machine on a two-symbol input has 693 variables,
DPLL solves it, and the assignment decodes into the machine's actual run.

## What is deliberately slow

Every solver here is brute force, except SAT which also has DPLL. That is the
point: NP is defined by the gap between checking and searching, and hiding the
search behind a clever algorithm would hide the definition.
