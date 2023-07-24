# Dining philosophers

Five philosophers, five forks, and a deadlock that appears at two philosophers
already.

| Philosophers | Naive | Ordered | Diners at once | Waiter limit |
|---|---|---|---|---|
| 2 | deadlocks | safe | 1 | 1 |
| 3 | deadlocks | safe | 1 | 2 |
| 4 | deadlocks | safe | 2 | 3 |
| 5 | deadlocks | safe | 2 | 4 |

The naive strategy has every philosopher take the left fork and then the
right. The ordered strategy numbers the forks and takes the lower number
first, which means exactly one philosopher (the last) reaches for its forks in
the opposite order to everyone else. That single asymmetry is the whole fix.

## Two independent checks agree

The interleaving search finds the deadlock by exploring states. The same
system modelled as a Petri net in [petri-nets](../../petri-nets/) has 14
reachable markings for three philosophers, and exactly one of them is a
deadlock: every philosopher holding a left fork, nobody able to continue. Two
different formalisms, the same answer, and the Petri net additionally names
the state rather than just reporting that one exists.

## Why breaking the cycle works

Deadlock needs four conditions together, and circular wait is the one this
problem makes visible. Ordering the forks makes a cycle impossible, because a
cycle would require some philosopher to hold a higher-numbered fork while
waiting for a lower-numbered one, and the ordering forbids that.

The waiter alternative attacks the same condition differently by admitting at
most n-1 philosophers to the table. With one seat empty at least one
philosopher can always complete, which is why the limit is n-1 and not
something cleverer.

## The number that surprises

Maximum concurrent diners is floor(n/2), so five philosophers eat two at a
time, not four. Forks are shared with both neighbours, so every eating
philosopher blocks two others. The problem is usually told as though the
interesting question were deadlock, and the throughput ceiling is the more
practical answer: a solution can be perfectly correct and still use less than
half the table.
