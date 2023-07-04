# Recovery

The log records the before and after image of every change. After a crash the
recovery reads it once forward to find the committed transactions, redoes
those, and undoes the rest in reverse order.

The example log has `t1` changing `a` from 10 to 20 and committing, and `t2`
changing `b` from 5 to 7 without committing. Recovery redoes `t1` and undoes
`t2`; applying it to the disk state `a = 20, b = 7` gives `a = 20, b = 5`.

## Write-ahead logging

The rule is that the log entry reaches stable storage before the data page
does. `wal_rule_holds` checks a sequence of log and write events for that and
rejects the order where the page goes first, because after a crash there
would be a changed page with no record of what it used to be, and the undo
would be impossible.

A checkpoint bounds the work: with a log of 1000 entries and a checkpoint at
900, recovery reads 100 instead of 1000.

The three failure kinds get three answers: a transaction failure is undone, a
system failure is undone and redone from the log, and a media failure needs a
backup plus the log since it was taken.
