# Deadlocks

Four conditions, all needed at once: mutual exclusion, hold and wait, no
preemption, circular wait. Breaking any one prevents the deadlock, and three
are usually impractical to break, which is why real systems attack the fourth
by acquiring locks in a fixed global order.

Verified directly: two processes taking the same two locks in the same order
cannot deadlock, and the same two taking them in opposite orders can.

## Detection is a cycle search

`find_cycle` returns the cycle rather than a boolean, because a detector that
reports a deadlock without saying who is in it leaves the operator with nothing
to kill.

## The banker's algorithm

A state is **safe** when some order exists in which every process can finish
from what is free plus what the earlier ones release. On the classic example
with five processes the safe sequence is `P1, P3, P0, P2, P4`.

Dropping two of those processes makes the same numbers **unsafe**: with only
P0, P1 and P2, the available `[3,3,2]` covers P1's need, and after P1 releases
its holdings nothing covers P0 or P2. Safety is a property of the whole state,
not of any process in it.

A request is granted only if it is within the declared need, within what is
available, **and** leaves a safe state. A system that checks only the first two
is doing bookkeeping, not avoidance.

## Why it is taught and not used

Every process must declare its maximum demand in advance, which almost none
can; the safety check runs on every request; and the set of processes changes
constantly. Real systems detect and recover, prevent by lock ordering, or
ignore the problem.
