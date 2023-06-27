# Pushdown automata

A finite automaton with a stack. The stack is the whole difference from the
first block, and it is exactly what lets a machine count: push on every `a`,
pop on every `b`, check the stack is empty.

## Nondeterminism is essential here

Unlike finite automata, where the subset construction removes the difference,
**deterministic pushdown automata accept strictly fewer languages**. Even-length
palindromes are the standard witness: the machine has to guess where the middle
is, and no deterministic one can.

That gap is why the course keeps nondeterminism throughout this level, and why
`accepts` runs a breadth-first search over configurations rather than following
one run.

## Two acceptance modes

By **final state** or by **empty stack**, equally expressive, with the
conversions in both directions here.

Both conversions push a fresh bottom marker under everything first. Without it,
converting to empty-stack acceptance would let the automaton empty the stack in
the middle of a run and accept a prefix of the input.

## The step limit reports what it knows

A pushdown automaton can loop on epsilon moves for ever while the stack grows,
so `accepts` bounds the search and rejects when the bound is reached. That is a
simulator reporting what it knows, and it is why membership is decided by
[CYK](../cyk/) instead: cubic and complete, with no bound to tune.
