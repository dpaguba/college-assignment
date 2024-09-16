# Parallel loops

The exercise sheets use OpenMP, where a loop becomes parallel by adding a
pragma. What the pragma hides is how the iterations are handed out and what
happens to variables written by more than one thread.

## Scheduling

Static scheduling assigns contiguous blocks before the loop runs, costs nothing
at run time, and assumes every iteration takes the same time. When one
iteration costs 100 and nine cost 1, static leaves one thread with 104 units
and the other with 5, while dynamic hands out iterations on demand and finishes
in 100.

Dynamic is not free: on a hundred equal iterations it performs a hundred
assignments against four, and each costs something. The choice is between a
known overhead and an unknown imbalance.

No schedule beats the longest single iteration, which both are checked against.

## Two failures that look nothing alike

A **race** is a correctness bug: two threads read and write a shared
accumulator and one update is lost. Simulated deterministically here, because a
real race appears once in a thousand runs and vanishes under a debugger.

**False sharing** is a performance bug: two threads write different variables
that share a cache line, and the line bounces between them. Two counters four
bytes apart generate a coherence message per iteration; the same counters a
cache line apart generate none. The program is correct either way.

## A reduction is not a faster critical section

A critical section serialises one update per iteration. A reduction gives each
thread a private accumulator and combines them once at the end, so the shared
write happens once per thread. Both are correct; only one scales.
