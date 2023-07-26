# Mutual exclusion

Four requirements, three failed attempts, and Peterson's algorithm, checked by
exhaustive interleaving rather than by argument.

| Attempt | States | Violates |
|---|---|---|
| single flag | 24 | mutual exclusion, bounded waiting |
| two flags | 12 | progress, bounded waiting |
| strict alternation | 6 | progress, bounded waiting |
| Peterson | 26 | nothing |

The state counts are small enough to read, and that is the argument for
checking this way. Every reachable combination of program counters and shared
variables is generated, so "this attempt is wrong" comes with the interleaving
that breaks it instead of a paragraph asking you to imagine one.

## What each failure teaches

The single flag fails because testing the flag and setting it are two steps.
Both processes read zero before either writes one, and both enter. The gap
between test and set is exactly what an atomic test-and-set instruction
removes, which is why hardware provides one.

Two flags fixes mutual exclusion by setting the flag before testing the
other's, and buys deadlock instead: both flags go up, both processes wait, and
neither backs off. Strict alternation removes deadlock by forcing turns, and
loses progress, because a process that never wants the critical section still
has to take its turn before the other can go again.

Peterson combines the two failed ideas. The flag says "I want in" and the turn
breaks the tie, with the turn variable set to the *other* process, so whoever
writes it last yields. Both requirements hold at once because the two
mechanisms cover each other's failure.

## Bounded waiting

The strict alternation and two-flag attempts fail bounded waiting as well,
which is worth separating from progress: progress asks whether anyone gets in,
bounded waiting asks whether a particular process gets in eventually. An
algorithm can satisfy the first and starve one participant forever, so the
checker tests them separately.
