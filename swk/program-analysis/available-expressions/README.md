# Available expressions

Which expressions have already been computed on **every** path to a point, and
not invalidated since.

```
kill([x := a]l) = every expression containing x
gen ([x := a]l) = subexpressions of a that do not contain x
gen ([b]l)      = subexpressions of b
```

Forward and *must*: joined with intersection, so an expression counts only if
every path computed it. Nothing is available at the entry, and every other
label starts from the full set so the iteration can shrink to the greatest
fixed point.

## Why gen subtracts the killed part

`x := x + 1` computes `x + 1` and then changes `x`, so the expression is not
available afterwards. Filtering the assigned variable out of `gen` is what
keeps that case right, and it is the one place where kill and gen interact
inside a single block.

## What counts as an expression

Arithmetic only: `+ - * / %`. Variables and literals are excluded because
they cost nothing to recompute, and comparisons and boolean operators are
excluded because the classical analyses are defined over AExp. A test still
contributes the arithmetic inside it.

That choice matters for the answers. Including comparisons changes the tables,
and the textbook results this was checked against use AExp.

## Verification

Checked against the standard example from Nielson, Nielson and Hankin:

```
[x := a+b]1; [y := a*b]2; while [y > a+b]3 do ([a := a+1]4; [x := a+b]5)
```

with entry sets `(empty, {a+b}, {a+b}, {a+b}, empty)` and exit sets
`({a+b}, {a+b, a*b}, {a+b}, empty, {a+b})`. Every cell matches.

## The application

Common subexpression elimination: an available expression need not be
evaluated again. `redundant_computations` lists exactly those places.
