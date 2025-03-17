# Reaching definitions

Which assignments can still be the last write to a variable at a given point.

A fact is a pair `(x, l)`: the assignment at label `l` may still be the
current value of `x` here. The pair `(x, ?)` means `x` may still be
uninitialised, and it is what makes the analysis useful.

## The equations

```
kill([x := a]l) = {(x, ?)} u {(x, l') : l' assigns to x anywhere}
gen ([x := a]l) = {(x, l)}
kill and gen of a test or a skip are empty

RDentry(l) = {(x, ?) : x in FV(S)}                     if l = init(S)
RDentry(l) = union of RDexit(l') for (l', l) in flow   otherwise
RDexit(l)  = (RDentry(l) \ kill) u gen
```

Forward and *may*: a definition reaches a label if it reaches it along **some**
path. The analysis ignores which branch a test would take, and that
over-approximation is exactly what keeps it decidable.

## Use before definition

The application the lecture names. A read of `x` at a label whose entry set
contains `(x, ?)` may happen before any write.

The report can be spurious, because the path that leaves `x` unwritten might
never be taken. It is never missed, which is the direction that matters for a
warning.

## Verification

Exercise sheet 6 gives a control flow graph, asks for kill, gen, entry and
exit per node, and publishes the marked solution. This implementation
reproduces that table exactly, all six rows.

Reconstructing the graph from the picture took one correction: the true branch
of node 5 loops back to node 4, not onwards. The published entry set for node
4 contains `x4` and `y3`, which can only arrive through a back edge, and
running the three candidate shapes against the solution settled which one.
That is the same trick used throughout this repository: when the drawing is
ambiguous, the graded answer disambiguates it.

The lecture's own example was checked too, where `x` is never assigned and
`(x, ?)` correctly survives to the end.
