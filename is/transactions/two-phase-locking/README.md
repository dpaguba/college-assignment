# Two-phase locking

A transaction has a growing phase and a shrinking phase: once it has released
a lock it may not take another. `is_two_phase` checks a sequence of lock and
unlock operations for that.

## The guarantee, simulated

`schedules_under_locking` runs a small lock manager over two transactions and
enumerates every schedule it could produce, using the compatibility matrix
(two shared locks coexist, everything else conflicts) and holding locks to
the end of the transaction.

With `t1 = r(a), w(b)` and `t2 = r(b), w(a)` there are 6 possible
interleavings and 4 of them are not conflict serialisable. The lock manager
produces exactly 2, both serial. The protocol does not check the conflict
graph; it makes the schedules that would have a cycle impossible to build.

The protocol is not simply serialising everything. With `t1` on `a` and `t2`
on `b`, all 6 schedules are allowed and 4 of them interleave, because the
transactions never ask for the same lock.

## Strict and basic

Basic two-phase locking guarantees serialisability but permits cascading
aborts: another transaction may have read a value that is later rolled back.
Holding the locks to the end of the transaction, the strict variant, prevents
that at the price of shorter concurrency windows.
