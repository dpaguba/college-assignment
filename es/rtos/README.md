# Real-time operating systems

| Topic | |
|---|---|
| [task-model](task-model/) | costs, periods, deadlines, and the simulator |
| [resource-access](resource-access/) | inheritance and ceiling |
| [priority-inversion](priority-inversion/) | the failure the protocols answer |

Chapter four. The block exists because sharing a resource breaks the
priority order: a high priority task can be delayed by a low priority one,
and without a protocol that delay is unbounded.

The interesting part is that a protocol is judged by what it lets the
analysis prove. Inheritance bounds the blocking by one critical section per
resource, the ceiling protocol by one in total, and it is that number, not
the elegance of the mechanism, that enters the response time equation.
