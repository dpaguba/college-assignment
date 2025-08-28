# Rechnerarchitektur

Eighteen modules in six blocks, following the course from what performance is
to what limits it.

| Block | |
|---|---|
| [performance](performance/) | Amdahl, the iron law, power |
| [pipelining](pipelining/) | the five stages, hazards, scheduling |
| [dynamic-scheduling](dynamic-scheduling/) | scoreboarding and Tomasulo |
| [branch-prediction](branch-prediction/) | one bit to tournament |
| [memory-hierarchy](memory-hierarchy/) | caches, replacement, the three Cs, AMAT |
| [parallelism](parallelism/) | parallel loops, coherence, networks |

## No published solutions

Unlike the other subjects in this repository, this course publishes no
solutions: the `exercises` files are the same sheets in English. Verification
therefore leans on independent oracles: a simulation against an analytic
formula, two algorithms on the same input, brute force on small inputs.

The one exercise with a checkable numeric answer is sheet 2, and it comes out
exactly: the program with 4% serial work, 70% capped at 16 units and 26%
unbounded reaches a speedup of exactly **10.000 at exactly 16 cores**, which is
the cap on the bounded part.

## Three results worth stating

**Renaming is worth 18 cycles on three instructions.** On the classic
`div, add, sub` example the scoreboard delays the subtraction's write-back from
cycle 6 to cycle 24, and both machines still finish in cycle 25. A total-cycle
comparison reports no difference at all, which is why the cost is measured per
instruction.

**A one-bit predictor is worse than a fixed guess.** On a loop of four taken
branches and one not taken it is right 65% of the time, against 80% for
"always taken", because it mispredicts twice per loop rather than once.

**A larger FIFO cache can miss more often.** Belady's anomaly, measured: 0.750
with three ways and 0.833 with four on the standard reference string, where LRU
goes the other way as a stack algorithm must.

## Deliberate overlap

Caches and pipelines also appear in `rechnerstrukturen`, which is the earlier
course; this one starts where that one stops, with dynamic scheduling,
prediction and multiprocessors.
