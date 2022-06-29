# Basic queries

The example database holds five presidents and four elections, in sqlite3, in
memory, rebuilt for every query so no test can affect another.

`agrees_with_engine` runs the same selection twice, once in SQL and once over
the Python list, and compares the sets. It is a small check with a purpose:
every other module in this block trusts the engine, so the first one shows
that the data going in is the data coming out.

## The order the clauses run in

Written: `SELECT … FROM … WHERE … GROUP BY … HAVING … ORDER BY`.
Evaluated: `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `SELECT`, `ORDER BY`,
`LIMIT`.

`SELECT` runs late, which is why an alias defined there cannot be used in
`WHERE` but can be used in `ORDER BY`. Most of the surprises in the rest of
this block come from that ordering.
