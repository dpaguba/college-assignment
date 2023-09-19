# Tomasulo's algorithm

An instruction waits for its operands, not for its predecessors. Reservation
stations hold instructions until their inputs arrive, and a register file entry
points at whichever station will produce its value rather than holding one.

That indirection **is** register renaming, and it removes the two false
hazards:

- **WAR** goes away because a reader captured the value or the tag at issue, so
  a later writer cannot disturb it
- **WAW** goes away because the register points at the last writer only

RAW stays, because it is a dependence of the computation.

## Measured against the scoreboard

On the classic example the subtraction writes in cycle **6** instead of **24**.
See [scoreboarding](../scoreboarding/) for the full table.

## Reservation stations are a real limit

Six independent multiplications with one station issue one at a time and take
far longer than the same six with six stations. Renaming removes the false
dependences and cannot remove the structural one, which is why a machine's
station count appears in its specification.

## The check that matters

Out-of-order execution must produce in-order results, so the final register
values are compared against a strictly sequential run. A reordering that is
faster and wrong is not an optimisation, and it is the only failure mode of
this algorithm that a cycle count would not reveal.
