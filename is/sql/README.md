# SQL

Six modules on a five-row example database in sqlite3: the basic clauses and
the order they actually run in, the join and what a forgotten condition
costs, grouping, subqueries, the three-valued logic, and views.

Half of the block is about nulls, because that is where SQL stops behaving
like the relational algebra: `COUNT(*)` and `COUNT(column)` disagree,
`NOT IN` returns nothing where `NOT EXISTS` returns two rows, and a row can
fail both a condition and its negation.
