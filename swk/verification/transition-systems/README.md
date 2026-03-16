# Transition systems

The model everything in this folder is verified against.

```
T = <s, I, G>
```

with `s` a set of typed variables, `I` a formula over `s` describing the
initial states, and `G` a formula over `s` and the primed copy `s'` describing
the transition relation.

## How the lecture arrives here

A component has state, inputs and outputs. Compose it with a **driver** that
supplies inputs and a **monitor** that watches outputs, and the result has
neither: a closed system, which is exactly a transition system.

Composition is conjunction. Two components side by side form one system whose
transition relation is the conjunction of theirs, with shared variable names
doing the wiring. That is why drivers and monitors need no special treatment.

## Why formulas and not code

Because `I` and `G` describe **sets** of states and pairs of states, not one
execution. A driver that picks any input in a range is a formula with several
models, and nothing has to enumerate them until a question is asked.

The state space is generally infinite, which is the reason everything
downstream is bounded, inductive, or symbolic rather than an exhaustive walk.

## What this module offers

`successors` solves the transition relation with the current state fixed, so a
deterministic system yields one successor, a non-deterministic one several,
and a stuck state none. `run` follows one path, which is enough for the closed
systems the composition produces.

Bounds appear here for the first time, in `domains`. They are not part of the
model; they are what makes the solver terminate.

## Verification

The exam's system, `I = (s1 = 20)` and `G = (s1' = s1 / 2)`, produces the path
20, 10, 5, 2, 1, and the property `s1 mod 2 = 0` fails at the third state,
which is what [bounded model checking](../bounded-model-checking/) then finds
on its own.
