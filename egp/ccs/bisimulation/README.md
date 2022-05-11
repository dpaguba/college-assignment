# Bisimulation

Two processes are strongly bisimilar when each can match every step of the
other and the results are again bisimilar. Computed here by partition
refinement: everything starts in one class, and states that reach different
classes are split until nothing changes.

## Why the language is not enough

`a.(b.0 + c.0)` and `a.b.0 + a.c.0` perform exactly the same sequences: a,
then b or c. They are different processes. The first decides after the a, the
second before it, so a partner who has done a and now wants b may be out of
luck with the second and never with the first.

## Exercise 6b, and the answer that looks right

Asked for a process without parallelism behaving like `a.0 | b.0 | c.0`, the
answer that suggests itself is the sum of the six orderings. The module
checks it and it is **not** bisimilar, though it has the same traces. After
the first a, the parallel composition still offers b and c; the flat sum has
already chosen an ordering and offers one of them.

The correct answer nests the choices:

`a.(b.c.0 + c.b.0) + b.(a.c.0 + c.a.0) + c.(a.b.0 + b.a.0)`

and `expand` builds it for any number of prefixes. That is the expansion law,
and the module verifies it rather than asserting it.
