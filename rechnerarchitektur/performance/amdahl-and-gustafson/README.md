# Amdahl's law and Gustafson's law

Both describe parallel speedup and they answer different questions. Amdahl
fixes the **problem** and asks how much faster more cores make it. Gustafson
fixes the **time** and asks how much bigger a problem the cores allow.

## The sheet's program

Parts A, C and E are serial and total 4%. Part B is 70% and splits into at most
16 pieces. Part D is 26% and has no limit.

| cores | speedup |
|---|---|
| 2 | 1.92 |
| 4 | 3.57 |
| 8 | 6.25 |
| 15 | 9.62 |
| **16** | **10.00** |
| 32 | 10.88 |
| 1000 | 11.90 |

The answer is exactly **16 cores**, and it is exactly the cap on part B. The
exercise is built so that the two coincide: at 16 cores every parallel part is
running at its maximum, and beyond that only D keeps improving.

The ceiling is 25, the reciprocal of the serial 4%, and the curve never gets
close: at 1000 cores it has reached 11.9, because B stopped contributing at 16.

## The two laws on the same program

Gustafson applied to the same 16 cores, with part D solving a problem twice as
large, gives a scaled speedup of **10.84**. Nothing about the machine changed;
the question did.

## Efficiency is the number a purchase decision uses

A speedup of 10 on 16 cores is an efficiency of 0.63. The same speedup on 64
cores would be 0.16, and both are "10 times faster".

## Verified against a mechanism

`amdahl` is checked against `simulate_runtime`, which divides the work up
rather than applying the formula. They agree for every combination tried, which
is what makes the formula a description of the mechanism rather than a
definition of it.
