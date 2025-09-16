# Loop optimisations

Code inside a loop runs many times, so moving work out of it, or making each
iteration cheaper, is worth more than the same change anywhere else.

## Finding the loop needs dominance, not reachability

A back edge goes to a node that **dominates** its source. Using reachability
instead is the tempting shortcut and it is wrong: in a graph whose loop is
reachable from the entry, the target of every earlier edge can reach that edge's
source through the loop, so the straight-line prefix is reported as extra loops.
On the test graph that meant 4 loops instead of 1.

Dominance distinguishes "goes back to the top of a loop" from "is followed by a
loop", and the natural loop of a back edge is its header plus everything that
reaches the source without passing the header. That single-entry property is
what makes every transformation below safe.

## The three transformations

| | found in the test loop |
|---|---|
| invariant code motion | `t = a*b`, whose operands never change in the loop |
| induction variables | `i`, updated as `i = i+1` |
| strength reduction | `t = i*4` becomes `t = i+i+i+i` |

Hoisting replaces the statement inside the loop with a skip and puts it on the
edge entering the header from outside. That edge is unique for a natural loop,
which is exactly why the transformation is correct: the computation runs once
per loop execution instead of once per iteration.

`x = t+i` is not invariant and is not moved, because `i` changes inside the
loop. The invariance test here is the cheap conservative one, every operand
assigned nowhere in the loop; a real optimiser iterates, since a statement
becomes invariant once what it depends on has been hoisted.

## Strength reduction has a cut-off

Replacing a multiplication by repeated addition pays only while the additions
are cheaper than the multiply. Four additions are cheaper on some machines and
not on others, so `i*4` is reduced and `i*7` is left alone. The judgement is in
the cut-off, not in the transformation.
