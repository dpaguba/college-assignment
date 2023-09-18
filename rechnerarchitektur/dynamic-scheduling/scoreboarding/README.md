# Scoreboarding

The CDC 6600's answer to out-of-order execution, ten years before Tomasulo and
one idea short. A scoreboard tracks which unit will write each register and
stalls on all three hazards:

| hazard | stalls the |
|---|---|
| structural | issue |
| WAW | issue |
| RAW | read operands |
| WAR | **write back** |

Because there is no renaming, the false hazards still cost.

## The classic example

    div f0, f2, f4      latency 20
    add f10, f0, f8     RAW on f0, waits
    sub f8, f8, f14     WAR on f8 with the add

| instruction | scoreboard writes at | Tomasulo writes at |
|---|---|---|
| div | 22 | 22 |
| add | 25 | 25 |
| **sub** | **24** | **6** |

The subtraction is ready in cycle 6 and may not write until the addition has
read the old `f8` in cycle 23. An **18-cycle** WAR stall, and both machines
still finish in 25 cycles, because the division is the critical path either
way.

That is why `false_hazard_cost` reports per instruction. A total-cycle
comparison of these two runs returns zero and hides the entire phenomenon.

## Two details that decide whether it works

A read waits only for a producer **earlier in program order**. Making a reader
wait for a later writer instead deadlocks the simulation: each waits for the
other.

The simulation reads the state at the start of a cycle and applies changes at
the end, the way synchronous hardware does. Updating in place makes the result
depend on the order the instructions happen to sit in the list, and lets a
dependent instruction read a value in the same cycle it was written, which is
one cycle too early.
