# Grammars and automata are the same thing here

Two constructions, and together they are the second equivalence theorem of the
course, matching Kleene's at the regular level.

## Grammar to automaton: short

One state. The stack holds the part of the sentential form still to be derived.
Two kinds of move:

```
(q, eps, A) -> (q, alpha)     for every rule A -> alpha      expand
(q, a, a)   -> (q, eps)       for every terminal a           match
```

The stack is exactly the unmatched suffix of the current leftmost sentential
form, which is why one state is enough: all the memory is in the stack.

## Automaton to grammar: cubic and unreadable

A variable `[p X q]` stands for "from state p with X on top, the automaton can
consume some input and end in state q with X gone". Every transition becomes a
rule threading intermediate states through the pushed symbols.

The number of variables is cubic in the size of the automaton, and the grammar
that comes back from a five-state machine is not something anybody reads. It is
a proof that the classes coincide, not an algorithm anybody runs, and the
module says so where the blow-up happens.

`round_trip` checks the claim the theorem actually makes: same language, on
`a^n b^n` and on balanced brackets.
