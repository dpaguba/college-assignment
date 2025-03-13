# The monotone framework

One worklist algorithm, four analyses.

Reaching definitions, live variables, available expressions and very busy
expressions differ in exactly four choices:

| | direction | combine | initial | what a fact is |
|---|---|---|---|---|
| [reaching definitions](../reaching-definitions/) | forward | union (may) | all undefined | `(variable, label)` |
| [live variables](../live-variables/) | backward | union (may) | empty | variable |
| [available expressions](../available-expressions/) | forward | intersection (must) | empty | expression |
| [very busy expressions](../very-busy-expressions/) | backward | intersection (must) | empty | expression |

Everything else is shared: the transfer function is always
`(incoming \ kill) | gen`, and the fixed point is always computed the same way.

## Why the abstraction is worth it

The correctness argument is made once. Each analysis then reduces to two
functions, `kill` and `gen`, and the framework guarantees the rest: that the
iteration terminates and that the answer is the least (or greatest) solution
of the equations.

## Termination

The sets only grow for a *may* analysis and only shrink for a *must* one, and
both are bounded by a finite universe. That is the ascending chain condition,
and it is the whole reason a lattice of finite height is required rather than
any collection of values. Drop it, as an interval analysis over the integers
does, and the iteration can run for ever, which is why such analyses need
widening.

## Worklist against chaotic iteration

Recomputing every label until nothing changes gives the same answer. The
worklist just avoids recomputing labels whose inputs did not change, and the
result reports how many recomputations it took.

## may against must

The difference is the direction the approximation errs in. A *may* analysis
over-approximates: it reports a fact if it holds along **some** path, so it
never misses one and can invent one. A *must* analysis under-approximates: it
reports a fact only if it holds along **every** path, so it never invents one
and can miss one.

Which is safe depends on the use. For "is this variable possibly
uninitialised", may is safe. For "can I skip recomputing this expression",
must is.

The starting value follows from that: a must analysis starts at the **full**
set everywhere but the entry, because intersection can only remove. Starting
it empty is sound and useless, since the answer stays empty.
