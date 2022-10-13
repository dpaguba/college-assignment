# M/M/1

One server, exponential inter-arrival and service times, first come first
served.

| Quantity | Formula |
|---|---|
| occupation rate | ρ = λ/μ |
| length of queue | L_q = ρ²/(1 − ρ) |
| waiting time | W_q = L_q/λ |
| cycle time | W = W_q + 1/μ |
| work in process | L = λ·W |

The lecture example: one order every 20 days, one completed every 10, so
λ = 0.05 and μ = 0.1. Then ρ = 0.5, L_q = 0.5, W_q = 10 days, W = 20 days,
L = 1.

## The call centre

260 calls between 8 and 17, of which 150 fall between 11 and 14. The peak
rate is 50 calls an hour, and the target is an average wait under one minute.

| Capacity | ρ | L_q | W_q | Target |
|---:|---:|---:|---:|---|
| 80 calls/h | 0.625 | 1.042 | **1.25 min** | missed |
| 90 calls/h | 0.556 | 0.694 | **0.83 min** | met |

Ten percent more capacity cuts the wait by a third. That is the shape of
1/(1 − ρ): near the top of the range, a small change in capacity buys a large
change in waiting.

`why_the_queue_explodes` puts numbers on it: at ρ = 0.5 half a case is
queueing, at 0.9 it is eight, at 0.99 it is ninety-eight.

## The check

`simulate` runs two hundred thousand customers with exponential gaps and
exponential service. At λ = 0.6, μ = 1 the formula gives W_q = 1.5 and the
simulation 1.49.
