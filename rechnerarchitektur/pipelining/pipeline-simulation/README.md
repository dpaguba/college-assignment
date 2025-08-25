# Pipeline simulation

Fetch, decode, execute, memory, write back. One instruction still takes five
cycles; five are in flight at once, so throughput approaches one per cycle
while latency does not change.

The simulation exists so that every claim about stalls comes out of a mechanism
rather than a formula. On 100 instructions the speedup over an unpipelined
machine is **4.808**, not 5: the pipeline has to fill, and the missing 0.192 is
that fill divided by the work.

## Stalls counted in issue cycles

A producer issued in cycle `p` computes in `p+2` and reaches memory in `p+3`.
So a consumer may issue at:

| case | earliest issue |
|---|---|
| forwarding, arithmetic producer | `p+1`, back to back is free |
| forwarding, load producer | `p+2`, one instruction of distance |
| no forwarding | `p+3`, the value comes from the register file |

On a three-instruction dependent chain that is 11 cycles and 4 stalls without
forwarding against 7 cycles and 0 with it.

## The fill is not a stall

The raw CPI of a program includes the four fill cycles, which for 60
instructions is 0.067 of CPI and has nothing to do with hazards. Comparing a
stall formula against a measurement means comparing the steady-state CPI, which
`steady_state_cpi` reports separately for exactly that reason.
