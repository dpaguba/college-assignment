# CPU scheduling

The algorithms differ in what they optimise. First come first served optimises
nothing. Shortest job first minimises average waiting time provably and needs
to know the future. Round robin bounds the response time at `(n-1) * quantum`
and pays a context switch per slice.

## Virtual round robin, on the sheet's processes

A (CPU 7, I/O 2), B (CPU 2, I/O 2), C (CPU 2, I/O 5), quantum 3 ms, first 30 ms.

Plain round robin gives a process that blocks early the same treatment as one
that used its whole slice: it goes to the back of the queue having used part of
its quantum, so it gets less CPU than it asked for.

Virtual round robin adds an **auxiliary queue** with priority, holding
processes returning from I/O, and lets them run for the **remainder** of the
quantum they gave up.

| | A | B | C |
|---|---|---|---|
| plain round robin | 14 | 9 | 6 |
| virtual round robin | 14 | **10** | 6 |

with 6 dispatches from the auxiliary queue in 30 ms. Both halves of the design
matter: the priority is what compensates the process that blocked, and the
remainder is what stops it from getting more than its share.

Verified as a simulation rather than asserted: no two processes run at the same
instant, no slice exceeds the quantum, every auxiliary dispatch is shorter than
a full quantum, and the auxiliary queue is always chosen when it is non-empty.
