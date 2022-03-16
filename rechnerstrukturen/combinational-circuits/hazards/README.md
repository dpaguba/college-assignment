# Hazards in combinational circuits

A circuit whose truth table is correct can still produce a wrong value while
its inputs change, because two paths through it have different delays.

A **static hazard** is a glitch where the output should have stayed constant.
It happens when two adjacent one-rows are covered by different terms and no
term covers both: as the input moves from one to the other, the first term
falls before the second rises.

## Measured

The cover `{ab', ab}` has a static hazard on the transition from `10` to `11`,
and the simulated trace is `1, 0, 1, 1`: the output dips although both
endpoints are one. Adding the consensus term `a` removes the dip, and the trace
stays at one throughout.

## The consensus term is redundant on purpose

It covers only rows the circuit already covered, so no output changes, verified
on every input combination. A minimiser therefore deletes it and reintroduces
the glitch.

That is the point worth keeping: **minimal and hazard-free are different
goals**. A design that has been minimised as far as possible is exactly the one
that glitches, and fixing it means adding back a term the minimiser was right
to remove by its own criterion.
