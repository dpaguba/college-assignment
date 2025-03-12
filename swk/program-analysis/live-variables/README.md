# Live variables

Which variables may still be read before they are overwritten.

```
kill([x := a]l) = {x}
gen ([x := a]l) = FV(a)
gen ([b]l)      = FV(b)
```

Backward, because liveness depends on what happens after a point. Joined with
union, because a variable is live if **some** continuation reads it. Nothing
is live at the end of the program.

## Dead assignments

A write to a variable that is not live afterwards computes something nobody
reads. Removing it cannot change the result, which is why every optimising
compiler runs this analysis, and why a linter can report it.

The direction of approximation is what makes the report trustworthy: liveness
is over-approximated, so an assignment reported dead is dead along every path,
not just some.

On the lecture example the analysis finds three: `z` is written at 2 and 4 and
never read, and the final `y := 0` writes a variable the program then
abandons.

Notice that the assigned variable is not part of `gen`. `x := x + 1` reads
`x`, so `x` is live before it; `x := 5` does not, so it is not. That
asymmetry is the whole reason the analysis can find dead writes at all.

## Where it stops

In a language with pointers, output or exceptions, "nobody reads it" stops
being a syntactic question. While has none of those, which is what makes the
analysis exact here and an approximation everywhere else.
