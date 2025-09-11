# Constant propagation

If a variable holds the same known value on every path to a point, its uses
there can be replaced by that value, and expressions built from constants can be
folded away entirely.

## The lattice is the analysis

Three levels: `UNDEFINED` at the top for "no path reaches here yet", the
constants in the middle, `UNKNOWN` at the bottom for "paths disagree".

    meet(c, c) = c              agreeing paths keep the constant
    meet(c, d) = UNKNOWN        disagreeing paths lose it
    meet(c, UNDEFINED) = c      an unreached path contributes nothing

Two branches assigning `a = 1` and `a = 2` give `UNKNOWN` after the join; two
branches both assigning `a = 1` keep the constant. The lattice has height two,
which is why the iteration terminates: a variable can only move down twice.

## Folding

    a = 3        a = 3
    b = a+1  ->  b = 4
    c = b*2      c = 8

Each folded statement needs no arithmetic instruction at all, and the constant
it produces enables the next fold. That chain is why the analysis is run to a
fixed point rather than in one pass.

## What it deliberately misses

Any unknown operand makes the result unknown, so `x - x` is not recognised as
zero. Catching that needs a relational domain, one that tracks facts about
pairs of variables rather than one value each, and the cost of that is a
different order of magnitude. The three-level lattice is the cheapest thing
that is useful, which is why it is the one every compiler ships.
