# Live variable analysis

A variable is **live** at a point when some path from there uses its current
value before overwriting it. Everything downstream depends on this one
definition: dead code elimination, register allocation, and the check that a
variable is initialised before use.

The analysis runs **backwards**, because liveness is about what happens after a
point, and takes **unions** at joins, because live on any outgoing path is
live. In the monotone framework that is the may-backward corner.

## The order inside the transfer function is not negotiable

    f(X) = (X \ kill) union gen

The sheet asks what happens when a programmer writes `(X union gen) \ kill`
instead. The answer is visible on one statement: for `y = y + b` with `y` live
afterwards, the correct order keeps `y` live, because the use is added after
the kill removes it. The wrong order removes it last and loses it.

On the sheet's graph the consequence is at node 5:

| | live at node 5 |
|---|---|
| correct | b, c, x, **y** |
| wrong | b, c, x |

and `y` really is live there: the path 5, 6, 7 reads it on the edge `y = y+b`
before assigning to it. `live_on_path` confirms it by search rather than by the
fixed point, which is what makes "the analysis is wrong here" a checkable claim
rather than an opinion. A live variable analysis is meant to over-approximate;
reporting a variable live when it is not costs a register, reporting one dead
when it is live breaks the program.

## The boundary condition changes the answer

What is live at the exit is a choice. Starting the exit with the empty set makes
the final value of every variable dead, so the last assignment to each is
removable. Starting it with **every** variable makes the final state observable.

On the sheet's graph the difference is not subtle: with an empty exit, five
assignments come out dead; with a full exit, exactly one does, `x = a+b`, which
is the published answer. The sheet's convention is the full one, and it is the
safe default for a procedure whose variables outlive it.

## The published analysis

| node | live |
|---|---|
| 1 | c, y |
| 2 | a, c, y |
| 3 | a, b, c, y |
| 4 | b, c, y |
| 5 to 8 | b, c, x, y |
| 9 | b, c, x |
| 10 | b, c, x, y |
| 11 | c, x, y |
| 12 | a, c, x, y |
| 13 | a, b, c, x, y |

`x` is not live at node 4, which is exactly why `x = a+b` on the edge into it
is dead.
