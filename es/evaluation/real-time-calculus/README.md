# Real-time calculus

A trace says what happened. An arrival curve says what can happen: the
maximum and minimum number of events in **any** interval of a given length,
over all positions of that interval. A bound derived from a curve holds for
every execution rather than for the one observed.

The exam's stream has two events at every period and one more at 0.3 of the
way through:

| Δ | upper | lower |
|---|---:|---:|
| 0 | 0 | 0 |
| 0.1p | 2 | 0 |
| 0.71p | 3 | 0 |
| p | 3 | 3 |
| 2p | 5 or more | 6 |

The upper curve jumps to 2 immediately, because two events can arrive at the
same instant and an interval of any positive length can cover both. The lower
curve stays at zero until a whole period has passed, because an interval
shorter than a period can always be placed to miss everything.

## Delay and backlog

The horizontal distance between the arrival curve and the service curve
bounds the delay; the vertical distance bounds the buffer. Both are computed
here, and when the arrival rate exceeds the service rate the distance grows
without limit and the module reports that there is no bound rather than the
largest value inside its horizon.
