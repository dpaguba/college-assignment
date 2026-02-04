# Budget instead of full runs

On each rung a fraction of the configurations survives and the survivors get
that same factor more budget. Both numbers move with the same factor, so every
rung costs the same, and the budget is not saved but redistributed.

| rung | configurations | budget each | total |
|---:|---:|---:|---:|
| 1 | 27 | 1 | 27 |
| 2 | 9 | 3 | 27 |
| 3 | 3 | 9 | 27 |
| 4 | 1 | 27 | 27 |

## What it saves

Eighty-one configurations, factor three: **405** units spent against **6 561**
for running all of them at the largest budget, a saving of 93.8 % while
examining exactly the same number of configurations.

## The configuration it cannot find

A configuration that looks bad early and would be the best at full budget is
cut on the first rung and never returns. Measured: rank 24 of 27 early, rank 1
late, and it does not survive.

The method assumes that the ranking at a small budget says something about the
ranking at a large one. For many learners that is roughly true, and for those
with a long warm-up it is not. The assumption can only be checked by running
some of the discarded configurations to the end, and that expense is rarely
paid.

## Hyperband

A single run has to decide between many configurations at little budget and
few at much, and which is right is not known in advance. Hyperband runs
several brackets, from 81 configurations at budget 1 down to 5 at budget 81,
and gives each roughly the same total.
