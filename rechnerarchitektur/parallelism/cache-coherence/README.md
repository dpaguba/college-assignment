# Cache coherence

With one cache per processor the same address can sit in several caches, and a
write in one makes the others wrong. MSI has three states: **Modified**, the
only copy and dirty; **Shared**, one of possibly several clean copies;
**Invalid**.

MESI adds **Exclusive**, the only copy and clean, and it exists for one
measurable reason.

## What the fourth state buys

Reading a line and then writing it:

| protocol | bus messages |
|---|---|
| MSI | 2 |
| MESI | **1** |

Under MSI the read leaves the line Shared, so the write must announce an
upgrade even though nobody else has a copy. Under MESI the read leaves it
Exclusive, so the write is silent. On uncontended data, which is most data,
that halves the traffic.

## Ping-pong is the worst case

Two processors writing the same line in turn cost a message per write: ten
rounds of two writes produce **20** messages. The traffic is proportional to
the number of writes, not to the amount of data, which is why two threads
updating adjacent counters can run slower than one thread doing both.

## The invariant, checked

At most one cache may hold a line Modified. Verified after each of four
processors writes in turn: the set of modified holders is always exactly the
last writer. A protocol that keeps two modified copies has lost, and no amount
of correct-looking transitions makes up for it.
