# CCS

A process is written down, and its behaviour is derived from three rules
rather than described. `a.P` can do `a` and become `P`; a choice offers both
sides; a parallel composition offers each side's moves plus a synchronisation
on complementary actions, which appears as the internal step `tau`.

```
(a.0 | 'a.0)        offers a, 'a, tau
(a.0 | 'a.0) \ a    offers tau only
```

Restriction is what turns "these two could communicate" into "these two must".
Hiding `a` removes the unsynchronised moves and leaves the handshake, which is
how CCS expresses that a channel is internal to a system.

## The three containers

| Capacity | Consecutive `in` | Greedy trace |
|---|---|---|
| 1 | 1 | in out in out in out |
| 2 | 2 | in in out in out in |
| 3 | 3 | in in in out in out |

A buffer of capacity n is n+1 constants, each offering `in` while there is
room and `out` while there is content. Capacity is visible in the behaviour
and stored nowhere, which is the habit CCS is teaching: the state is the
process.

Stack and queue have the same alphabet, the same actions available at every
point, and the same traces of action names. They differ only in which value
comes back after two pushes and two pops, `1 0` against `0 1`. Distinguishing
them needs the values in the labels, and that is why the course defines
containers by their observable output rather than by their storage.
