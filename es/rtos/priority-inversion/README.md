# Priority inversion

A high priority task waiting for a resource held by a low priority one is
unavoidable and bounded. The failure is what happens next: a medium priority
task, needing no resource at all, preempts the low priority holder, and the
high priority task now waits for work that has nothing to do with it.

The scenario, simulated:

| protocol | the high priority task waits |
|---|---:|
| none | 7 |
| inheritance | 2 |
| ceiling | 2 |

Without a protocol the wait is as long as the medium task runs, which nothing
in the system bounds. That is the failure that reset the Mars Pathfinder
repeatedly on the surface of Mars, and the fix deployed to it was priority
inheritance, enabled by a flag the mission had left off.
