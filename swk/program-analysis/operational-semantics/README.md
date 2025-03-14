# Structural operational semantics

The seven rules that say what a While program *does*, and the derivation they
produce.

```
<skip, v>                     => v                                  [SKIP]
<x := a, v>                   => v[x -> value]                      [ASS]
<if b then S1 else S2, v>     => <S1, v>   if b holds               [IF_T]
<if b then S1 else S2, v>     => <S2, v>   if b fails               [IF_F]
<while b do S, v>             => <S; while b do S, v>  if b holds   [WH_T]
<while b do S, v>             => v                     if b fails   [WH_F]
```

plus the two composition rules that carry a step through a sequence.

## Why write the semantics down at all

Because natural language is not precise enough. The lecture's own example is a
procedure that increments a global and returns 3, and asks what `x + awkward`
evaluates to: the answer depends on evaluation order, and English does not
fix one. A rule system does.

## The shape of the rules

Two axioms finish a statement and turn a configuration into a **state**: after
`SKIP`, `ASS` and `WH_F` nothing is left to run. The others produce another
**configuration**, so something remains.

The composition rules are where the recursion lives. `COMP_1` fires when the
first statement stepped to another configuration, `COMP_2` when it finished.
Sequencing needs no rule of its own beyond those two.

A loop is not unrolled statically. `WH_T` rewrites `while b do S` into
`S; while b do S`, one iteration at a time, which is how a finite rule system
describes an unbounded execution.

## The trace

`trace` returns every rule application with the configuration before and
after, which is the derivation an exam asks to be written by hand. On the
lecture's example with `x = 2` it produces the same intermediate states the
slides list: `v2`, `v3`, `v4`.

## Termination

`while [true]1 do [skip]2` never finishes, and nothing in this folder can
decide in general whether a program will. The step limit turns that into an
exception rather than a hang, which is a practical choice and not a solution.

## Verification

The trace was compared with the lecture's derivation, and the interpreter with
hand-computed results for the conditional, the loop and the non-terminating
case.
