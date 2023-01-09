# SQL

Six modules against a real sqlite3 database, following tutorials five to
eight.

| Module | Topic |
|---|---|
| [ddl](ddl/) | CREATE, ALTER, DROP and the order they must run in |
| [dml](dml/) | INSERT, UPDATE, DELETE and the population |
| [select-single-table](select-single-table/) | one table, no aggregates |
| [select-join](select-join/) | several tables |
| [aggregates](aggregates/) | COUNT, SUM, MIN and the traps |
| [group-and-having](group-and-having/) | grouping and conditions on groups |

Each module carries its own copy of the schema and the population, so each
folder runs on its own. The duplication is deliberate: these are teaching
artefacts meant to be opened one at a time, and the data is data rather than
logic.

Every query is checked against the same figures counted in Python from the
tuples. Two paths, one answer.
