# Minimisation

The smallest DFA for a language, and the reason it is unique.

Two states are equivalent when no word tells them apart. Merging equivalent
states loses nothing, and what remains is minimal **and unique up to
renaming**, which turns minimisation into a decision procedure: two DFAs accept
the same language exactly when their minimal automata are isomorphic.

## Two algorithms

| | Cost | Gives |
|---|---|---|
| table filling | O(n²·|Σ|) | which word separates each pair |
| Hopcroft | O(n log n) | the partition, nothing else |

Table filling marks pairs that are already separated by the empty word, then
repeatedly marks a pair whose successors are marked. The word that separated
the successors, with that symbol in front, separates this pair, and recording
it gives `separating_words`, which is what an exercise asks for.

Hopcroft refines a partition and always processes the **smaller** half of a
split, which is where the log factor comes from.

Both are implemented and checked against each other on every random automaton
in the test sweep: same size, isomorphic result.

## The trap state counts

`minimise` keeps the automaton **complete** by default, so the trap is a state.
That matters for the Nerode index: the words with no continuation into the
language form a class of their own, and dropping the trap gives a smaller
partial automaton whose state count is no longer the index.

This was a real bug here. With trimming on by default the exercise's automaton
reported an index of 2 instead of 5, because the dead class had been optimised
away. `keep_trap=False` still gives the smaller partial automaton when that is
what is wanted.
