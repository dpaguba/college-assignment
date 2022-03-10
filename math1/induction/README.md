# Induction

| Topic | |
|---|---|
| [inductive-definitions](inductive-definitions/) | the smallest set closed under rules |
| [structural-induction](structural-induction/) | claims over every structure, and counterexamples |
| [well-founded-orders](well-founded-orders/) | why induction and recursion work at all |

Defining and proving are the same operation seen twice. A set defined by
rules is the least fixed point of the operator those rules describe, and
induction over it is the statement that nothing else is in the set. That is
why the same computation, iterating to a fixed point, appears in this block,
in the closure of a relation, and in the order chapters as the theorem of
Knaster and Tarski.

The concrete result worth keeping is the term count: two constants and one
binary operation give 2, 6 and 38 terms at the first three depths, not 42.
The recurrence counts terms of the next depth, and the terms already built
are not new.
