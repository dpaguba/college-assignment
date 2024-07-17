# Closure properties

The operations regular languages survive, each as a construction.

| Operation | Construction | Result |
|---|---|---|
| intersection, union, difference | product automaton | DFA |
| complement | swap accepting states, after completing | DFA |
| concatenation | join with epsilon edges | NFA |
| star | fresh start, loop back | NFA |
| reversal | turn every edge around | NFA |
| homomorphism | expand each edge into a chain | NFA |

## The product automaton

States are pairs, both components move together, and the accepting set decides
which operation it is. One construction, four operations, which is why the
exercises keep coming back to it.

## Two constructions that are wrong in the obvious version

**Complement** needs the automaton completed first, or the words that had no
run stay rejected instead of becoming accepted. And the complement is always
relative to an **alphabet**: over `{a}` the complement of `a*` is empty, over
`{a, b}` it is everything containing a `b`. The parameter is explicit here so
that choice cannot be made by accident.

**Star** needs a fresh start state that is accepting. Reusing the old start and
making it accepting adds every word that happens to loop back to it, which is
the standard wrong construction and accepts too much.

## What the cross-check found

Comparing all four operations against direct word testing on 80 random language
pairs gave 249 disagreements at first, every one on a pair of languages over
**different alphabets**: an automaton that had never seen `b` got stuck on it
instead of rejecting. Extending both automata to the common alphabet before
combining fixed it, and the same sweep now agrees everywhere.
