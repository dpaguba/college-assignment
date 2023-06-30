# Deadlocks

An edge from `t1` to `t2` in the wait graph means `t1` waits for a lock `t2`
holds. A cycle in that graph is a deadlock, and a chain without a cycle is
merely a queue.

`cycle` returns the transactions involved and `victim` picks the one whose
abort costs least, by whatever measure of work done is passed in. The choice
matters: aborting the transaction that has done the most work throws away the
most, and always aborting the same one starves it.

## Four ways to handle it

Detection runs the cycle search periodically and aborts a victim. Prevention
orders the resources so a cycle cannot form; `ordering_prevents` checks
whether all transactions request in the same order, and two transactions
asking for `a, b` and `b, a` fail that test. Avoidance uses timestamps to
decide who waits and who dies. A timeout is the cheap version, and its
weakness is stated plainly: it cannot tell a deadlocked transaction from a
slow one, so it kills healthy transactions too.
