# Very busy expressions

Which expressions will certainly be computed **before** any of their variables
change.

Backward and *must*, the mirror image of
[available expressions](../available-expressions/). Together the four
analyses fill the two-by-two square that organises the whole subject:

| | may (union) | must (intersection) |
|---|---|---|
| **forward** | reaching definitions | available expressions |
| **backward** | live variables | very busy expressions |

## The difference from available expressions

`gen` does not filter out the assigned variable. In `x := a + b`, the
expression `a + b` **is** evaluated at this point, before the assignment takes
effect, and that is all busyness claims. Available expressions asks the
opposite question, whether the value is still good afterwards, so there the
filter is needed.

## The application

Code hoisting. An expression that is very busy at a point can be computed
there once, and every path below it then reuses the value instead of computing
it again. It saves work on all paths but one, and it is one of the few
optimisations that can make code *larger* in exchange for being faster.

## Verification

Checked against the standard example from Nielson, Nielson and Hankin:

```
if [a > b]1 then ([x := b-a]2; [y := a-b]3) else ([y := b-a]4; [x := a-b]5)
```

Both `a-b` and `b-a` are very busy at the test, because whichever branch is
taken computes both. The computed table matches the textbook, including the
empty exit sets at 3 and 5.
