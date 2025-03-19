# The While language

Syntax, labels, and the four control flow functions everything else is built
on. Lecture SWK-4, "Programm Analyse".

```
[y := x]1; [z := 1]2;
while [y > 1]3 do ([z := x * y]4; [y := y - 1]5);
[y := 0]6
```

## Why a language this small

While has assignment, sequence, conditional and loop, and nothing else. It is
Turing complete, so nothing is lost in principle, and every analysis fits on a
page. Adding procedures, pointers or exceptions is what makes real static
analysis hard; leaving them out is what makes the ideas visible.

## Labels are the point

Every elementary block carries a label, and the labels are unique. Analyses
key their results by label, so `parse` rejects a program that reuses one
rather than producing quietly wrong tables later.

Composition carries no label of its own. A sequence is not an elementary
block, and the lecture labels only assignments, skips and tests.

## The four functions

| Function | Meaning |
|---|---|
| `blocks(S)` | every elementary block, keyed by label |
| `init(S)` | the label that runs first, a single label |
| `final(S)` | the labels that can run last, a set |
| `flow(S)` | pairs of labels that can follow each other |

`final` is a set because a conditional can end in either branch. A loop ends
at its own test, because leaving the loop means the test failed.

`flow` of a loop is the interesting case: an edge from the test into the body
and an edge back from every final label of the body. The edge that leaves the
loop is not there. It comes from whatever follows the loop in a sequence,
which is why the flow relation is defined by structural recursion and not by
looking at the loop alone.

On the lecture's example `flow` gives exactly
`{(1,2), (2,3), (3,4), (4,5), (5,3), (3,6)}`, which is the graph drawn on the
slide.

## The example is not a factorial

`LECTURE_EXAMPLE` looks like one and is not: the body assigns `z := x * y`
rather than `z := z * y`, so each iteration overwrites the product. The
lecture uses it for control flow, not for arithmetic, and the constant's
docstring says so, because the name would otherwise mislead every reader of
the analyses that import it.

## Verification

The flow relation, `init` and `final` were checked against the lecture slide,
and the parser round-trips every program in this folder's examples.
