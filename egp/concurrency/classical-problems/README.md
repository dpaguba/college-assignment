# The four classical problems

Mutual exclusion, producer and consumer, readers and writers, dining
philosophers. They are patterns rather than puzzles: every concurrent system
contains at least one, usually several, and the solutions differ only in
their packaging.

## The philosophers

If every philosopher reaches for the left fork first, a state is reachable in
which each holds exactly one fork and waits for the next: a cycle of waiting
with no way out. If one of them reaches in the opposite order, two of them
compete for the same first fork, the cycle does not close, and the deadlock
becomes impossible.

Four conditions must all hold for a deadlock: mutual exclusion, hold and
wait, no preemption, and circular wait. Breaking any one is enough, and the
turned philosopher breaks the fourth.

## The other three

The bounded buffer needs two conditions: never take from an empty buffer,
never add to a full one. Readers and writers allows any number of readers or
exactly one writer, and its difficulty is not the rule but the fairness: a
steady stream of readers can keep a writer waiting for ever, and the remedy
is to queue arriving readers behind a waiting writer.
