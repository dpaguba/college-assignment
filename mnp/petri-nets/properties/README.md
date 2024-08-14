# Properties

Liveness, boundedness, safety, and place invariants.

| Property | Meaning | Read from |
|---|---|---|
| live | every transition remains possible from every reachable marking | the graph |
| deadlock | a reachable marking enabling nothing | the graph |
| bounded | some limit on tokens per place | the graph, or an invariant |
| safe | that limit is 1 | the graph |

A cycle of two places and two transitions is live, safe, and free of
deadlocks. The exercise-sheet net is safe and not live, because it ends in
`{P4: 1}` where nothing is enabled. Termination and liveness are opposites
here, and which one is wanted depends on whether the net models a system or a
procedure.

## Invariants

The incidence matrix C has one row per place and one column per transition,
and the solutions of x·C = 0 are weightings of places whose weighted token
count no firing can change. For the sheet net the basis is a single vector:

```
M(P1) + M(P2) + M(P3) + M(P4) = 1
```

One equation, proved by linear algebra, that bounds every reachable marking at
once, including markings nobody enumerated. It also explains the safety result
rather than merely reporting it: the token count is conserved, so no place can
ever hold two.

## The basis is not unique

For the mutual-exclusion net (two processes, one key) the computed basis comes
out as `{a1, a2}`, `{b1, b2}` and `{key} - {a1} - {b1}`, where the third has
mixed signs. Adding the first two to it gives

```
M(key) + M(a2) + M(b2) = 1
```

which is the invariant a textbook prints, and it says that at most one process
is in its critical section. Both descriptions span the same space. A solver
returns whichever basis its elimination order produces, so reading a raw
invariant basis takes a step of combination before it says anything
recognisable.
