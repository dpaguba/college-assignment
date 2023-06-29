# ACID

Atomicity, consistency, isolation, durability. The transfer function shows
the first one: with `fail_midway` the balance stays at 100 and the target
stays at 0, because a transaction that does not reach its end leaves nothing
behind, not even the half it had already done.

## Isolation levels

| level | dirty read | non repeatable read | phantom |
|---|---|---|---|
| read uncommitted | yes | yes | yes |
| read committed | no | yes | yes |
| repeatable read | no | no | yes |
| serializable | no | no | no |

Each step up removes one anomaly and costs concurrency. The table is the
whole content of the isolation level: a level is defined by what it still
allows, not by how the system implements it.

Durability rests on the log. The log entry is written before the commit
returns; the data pages may follow later, which is what makes a crash
recoverable at all.
