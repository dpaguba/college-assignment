# Decision algorithms

Everything natural about regular languages is decidable. That stops one level
up: for context-free languages, equivalence is already undecidable.

| Question | Method | Cost |
|---|---|---|
| word in language | run the automaton | O(length) |
| language empty | reachability from the start | O(states + edges) |
| language finite | look for a cycle in the trimmed automaton | O(states + edges) |
| languages equal | symmetric difference is empty | product, then reachability |
| inclusion | difference is empty | product, then reachability |
| universality | complement is empty | complete, then reachability |

## Emptiness and finiteness are graph questions

The language is non-empty exactly when an accepting state is reachable, and the
shortest path to one is the shortest word. It is infinite exactly when the
**trimmed** automaton has a cycle: everything in a trimmed automaton is both
reachable and useful, so any cycle can be run any number of times.

Trimming first is what makes the cycle test correct. A cycle among dead states
says nothing.

## Equivalence, computed twice

`equivalent` runs both methods, the symmetric difference and the isomorphism of
the minimal automata, and raises if they disagree. They cannot disagree, and
checking is free next to the cost of being wrong quietly. That assertion is
what caught the alphabet bug described in
[closure-properties](../closure-properties/).

## The alphabet is part of the question

`a*` reports as universal, and that is correct: over its own alphabet `{a}` it
accepts everything. Over `{a, b}` it does not. Every question here is relative
to an alphabet, and the module extends both automata to the common one before
comparing.
