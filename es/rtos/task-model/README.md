# The task model

A real-time task is a cost, a period and a deadline, and the three arrival
patterns decide which analysis applies:

| kind | arrivals |
|---|---|
| periodic | exactly every T |
| sporadic | at least T apart |
| aperiodic | no bound |

Only the first two can be analysed, because only they bound the demand. That
is the reason aperiodic work is handled by a server with a budget rather than
by a schedulability test.

The module also holds the simulator the rest of the subject is checked
against. It runs a task set one time unit at a time under a chosen policy and
reports which task ran and which deadlines were missed. It assumes nothing
and is far slower than any test, which is what makes it an oracle rather than
an alternative.
