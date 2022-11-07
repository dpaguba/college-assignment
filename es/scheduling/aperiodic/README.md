# Aperiodic jobs

With every job available at once, ordering by deadline minimises the maximum
lateness. That is Jackson's rule, and the module checks it against every
permutation rather than citing it.

The exam's set:

| job | C | d |
|---|---:|---:|
| τ1 | 8 | 24 |
| τ2 | 2 | 9 |
| τ3 | 9 | 14 |

Earliest due date gives τ2, τ3, τ1 with completions 2, 11 and 19, all inside
their deadlines, so the set is feasible.

## Arrivals change the question

With release times the rule becomes earliest deadline first, and it is
optimal only with preemption. The module includes a set that is feasible with
preemption and infeasible without it: a long job started at time zero cannot
be interrupted for a short one that arrives at time one with a tighter
deadline.

That is the general shape of the topic. Every scheduling result holds under
assumptions about arrival, preemption and cost, and dropping one of them
usually costs optimality rather than merely efficiency.
