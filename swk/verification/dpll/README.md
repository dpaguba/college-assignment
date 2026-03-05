# DPLL

The satisfiability algorithm from the lecture, with the trace it produces.

Davis, Putnam, Logemann and Loveland, 1962. Backtracking search plus two
observations that skip whole subtrees:

- **unit clause**: a clause with one unassigned literal has only one way to be
  satisfied, so that assignment is forced rather than guessed
- **pure literal**: an atom occurring with a single sign can take that sign
  without ever hurting

## The lecture's example

```
(x1 or x2) and (not x2 or x3) and (x2 or not x3)
```

```
x1 := 1   [pure]
x2 := 0   [split]
  x3 := 0   [unit]
```

Three variables, eight possible assignments, one tested. That gap is the whole
argument for the two rules, and the implementation reproduces the slide's
trace exactly.

## Still exponential

The worst case is O(2^n) and no rule here changes that. SAT is NP-complete, so
a polynomial algorithm would settle P versus NP. What DPLL buys is that the
average case, on the structured formulas that verification produces, is
nothing like the worst case.

## Trusting the answer

A solver saying SAT is only useful if the model can be checked, and
`check_model` does that independently of the search. Every random instance in
the verification of this folder had its model checked, not just its verdict.

## Verification

The lecture trace, and 400 random CNF instances against the brute force
reference, with every returned model validated.
