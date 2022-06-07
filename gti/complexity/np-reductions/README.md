# Reductions between NP problems

```
SAT  ->  3SAT  ->  CLIQUE  ->  VERTEX COVER
               ->  INDEPENDENT SET

HAMILTONIAN CYCLE  ->  TSP
```

Cook and Levin proved SAT complete directly. Every completeness proof since is a
chain from there, and this is the chain the course walks.

## Each reduction transports certificates too

Transforming the instance is half the job. The other half is turning a solution
of the target back into a solution of the source, and that is what an exercise
means by "explain the correspondence":

| Reduction | Certificate map |
|---|---|
| 3SAT to CLIQUE | each chosen vertex is a literal that must be true |
| CLIQUE to VERTEX COVER | the vertices **outside** the cover form the clique |
| 3SAT to INDEPENDENT SET | the same as the clique case, edges inverted |
| HAMILTON to TSP | the tour is the cycle, read through the vertex order |

## Verified in both directions

Every link was checked on random instances: the yes-instances line up, **and**
the transported certificate passes the source verifier.

| Reduction | Instances | Result |
|---|---|---|
| SAT to 3SAT | 60 formulas | satisfiability preserved |
| 3SAT to CLIQUE | 40 formulas | preserved, certificates transport |
| CLIQUE to VERTEX COVER | 40 graphs | preserved, certificates transport |
| 3SAT to INDEPENDENT SET | 40 formulas | preserved, certificates transport |
| HAMILTON to TSP | 30 graphs | preserved, certificates transport |

## The one case worth reading twice

`sat_to_three_sat` on a clause of more than three literals chains them through
fresh variables. The fresh variables act as a carry: a satisfying assignment
fixes them, and if none of the original literals is true the chain forces a
contradiction. The padding cases for one and two literals are easier and are
where an off-by-one usually hides, which is why all four are tested.
