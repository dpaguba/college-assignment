# CDCL

What modern SAT solvers do instead of plain backtracking.

DPLL backtracks one decision at a time and forgets what it learned. Conflict
driven clause learning keeps three things:

- an **implication graph**, recording why each assignment was forced
- a **learned clause** derived from each conflict, forbidding the cause rather
  than the symptom
- a **backjump** to the level where that clause becomes useful, often far
  above the last decision

## The learned clause is the idea

A conflict deep in the search usually has a small explanation. Resolving the
falsified clause against the reasons on the trail, until only one literal from
the current decision level remains, produces that explanation: the first
unique implication point. Adding it as a clause stops the same mistake from
being repeated anywhere else in the tree.

The clause is *asserting*: right after the backjump it is unit, so the search
continues immediately instead of re-deciding.

## Where it does not help

The pigeonhole formulas, `holes + 1` pigeons into `holes` holes, are
unsatisfiable and have no short resolution proof at all. Haken proved in 1985
that every resolution refutation of them is exponential, and clause learning
is a resolution method, so it inherits the bound. The numbers show it:

| holes | conflicts | time |
|---|---|---|
| 5 | 149 | 0.05 s |
| 6 | 485 | 0.45 s |
| 7 | 1517 | 5.8 s |

Roughly a factor of three per hole. That is the counterweight to
"modern SAT solvers handle millions of clauses": they handle the structured
instances that come out of verification, not every instance.

## Verification

400 random CNF instances against brute force, every model independently
checked, and the pigeonhole family for the growth curve.
