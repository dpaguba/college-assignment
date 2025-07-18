# Heuristics

Local search improves a solution until no neighbour is better, which is a
local optimum and need not be the global one. That is the definition of the
method rather than a flaw in it, and the module exhibits a landscape where it
happens.

Simulated annealing accepts a worse solution with a probability that falls
over time, so it can leave a local optimum early and settle later. On the
same landscape it reaches a better value than the local search does.

## What a heuristic cannot report

| method | bound on the gap |
|---|---|
| branch and bound | the relaxation bounds the optimum |
| dynamic programming | exact by construction |
| local search | none |
| simulated annealing | none |

That is the whole difference. An exact method can say how far from optimal it
might be; a heuristic returns a solution and no statement about it, and any
claim about its quality has to come from somewhere else.
