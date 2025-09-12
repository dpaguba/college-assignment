# Dead code elimination

An assignment is dead when its target is not live immediately after it.
Finding them is one liveness analysis; the reason this needs its own module is
that **removal changes the analysis**.

## The published two rounds

| round | removed | why |
|---|---|---|
| 1 | `x = a+b` on edge (3,4) | `x` is overwritten at (4,5) before any use |
| 2 | `a = 1` on edge (1,2) | removing round 1 took away the last use of `a` |

After round 1 the liveness sets change at exactly two nodes, 2 and 3, and what
changes is that `a` disappears from both. That is what makes `a = 1` dead.
Removing it changes nothing at node 1, so the process stops after two rounds
with nothing dead left.

A single pass would have found one of the two. That is the whole argument for
iterating, and it generalises: every optimisation that removes code can expose
more of the same kind.

## Removal keeps the edge

A dead assignment becomes a skip rather than disappearing. Deleting the edge
would change the control flow, which is a different transformation with
different conditions. Conditions are never removed at all: they steer the
program whatever their value is used for.

## The exit convention decides how much is dead

With every variable live at the exit, two assignments go. With nothing live at
the exit, five do, including `x = 2y-1`, `a = 0` and `b = 0` whose results are
genuinely never read inside the fragment. Neither answer is wrong; they answer
different questions about what happens after the last node.
