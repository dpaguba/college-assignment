# Predicate logic

| Topic | |
|---|---|
| [structures-and-models](structures-and-models/) | what a formula means in a structure |
| [normal-forms](normal-forms/) | prenex form, Skolemisation, clause form |
| [herbrand-expansion](herbrand-expansion/) | reducing first-order unsatisfiability to propositional |
| [unification](unification/) | Robinson's algorithm and the occurs check |
| [resolution-and-prolog](resolution-and-prolog/) | resolution with unification, and SLD resolution |

## The arc

First-order logic is undecidable, so no procedure can answer every question
about it. What exists is a **semi-decision** procedure for unsatisfiability, and
the four modules after the first are the steps of building one:

1. get to clauses, giving up equivalence for satisfiability along the way
2. reduce to propositional logic over ground terms, by Herbrand's theorem
3. avoid enumerating those terms, by unifying instead
4. restrict to Horn clauses and get a programming language for free

Each step is an improvement on the previous one and none of them changes what
is decidable. The undecidability shows up as non-termination on satisfiable
input, in exactly the same place at every step.
