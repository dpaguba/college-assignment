# Optimistic locking

A version column, raised on every write. An update states which version it
read; if the row has moved on, the update is refused.

## The lost update, measured

Two transactions read version 0. The first writes and the row becomes version
1. The second writes:

- with locking: refused, and the first change survives;
- without: it succeeds, and the first change is gone with nobody informed.

The module returns which value survived and whether the second write was
refused, for both cases.

## Against pessimistic locking

Optimistic locking fails at commit; pessimistic locking waits at read. The
first suits short transactions with few conflicts, the second long ones with
many. Optimistic locking needs a retry loop, which is where the work is: read
again, reapply, and try once more.
