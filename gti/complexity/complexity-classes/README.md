# P, NP and what the classes mean

```
P    decidable in polynomial time
NP   certificates checkable in polynomial time
```

The second phrasing is the working one, and every problem in
[np-problems](../np-problems/) is written in that shape: a fast verifier, a slow
search.

P is contained in NP, because a decider is a verifier that ignores the
certificate. Whether the containment is strict is open, and nothing here
settles it.

## The gap, measured

Searching for a clique of size 4 against verifying one:

| n | certificates | search | verify |
|---|---|---|---|
| 6 | 15 | 0.00002 s | 0.00000013 s |
| 12 | 495 | 0.00015 s | 0.00000171 s |

The verify column is flat and the certificate column grows as a binomial. That
picture is all NP is: checking does not care how many candidates there were.

## Decision against optimisation

NP-completeness is defined for **decision** problems, and every optimisation
problem has a decision twin: instead of "what is the best value", ask "is a
value of at least k reachable".

They are equally hard up to a polynomial factor, and the module shows both
directions. `optimise_by_binary_search` recovers the optimum from a decider in
a logarithmic number of calls: for a range of 0 to 100 it takes **6**. That is
exercise 11.4, and it is why the theory can restrict itself to decision
problems without losing anything.

## The classes in one table

| Class | Means |
|---|---|
| P | decidable in polynomial time |
| NP | certificates checkable in polynomial time |
| NP-hard | every NP problem reduces to it |
| NP-complete | in NP **and** NP-hard |
| co-NP | complements of NP problems, such as unsatisfiability |
