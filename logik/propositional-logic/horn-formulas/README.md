# Horn formulas

A Horn clause has at most one positive literal, so it reads as an implication
with a conjunction of conditions and a single conclusion:

| clause | reads as | role |
|---|---|---|
| `{C}` | `true -> C` | fact |
| `{!A, !B, C}` | `A and B -> C` | rule |
| `{!A, !B}` | `A and B -> false` | goal |

Satisfiability for Horn formulas is linear, while the general problem is
NP-complete. The algorithm is one paragraph: mark what is forced, repeat, and
report unsatisfiable when a goal clause has all its conditions marked.

## The marking is a fixed point with a bound

On `A`, `A -> B`, `B -> C`, `C -> D` the marking proceeds

    {} -> {A} -> {A,B} -> {A,B,C} -> {A,B,C,D}

Each round marks at least one new variable, so there are at most as many rounds
as variables, and each round is one scan of the clauses. That is where the
linear bound comes from.

## The minimal model is the real payoff

The marked set is not merely **a** model, it is contained in **every** model: a
variable is marked only when some clause forces it. A general propositional
formula has no such canonical model, and that difference is why Horn clauses
are the basis of logic programming. A Prolog program has a well-defined answer
precisely because its minimal model is unique.

Verified two ways: the algorithm agrees with brute force over all assignments
on four sample formulas, and the marked set is contained in every satisfying
assignment enumerated by hand.
