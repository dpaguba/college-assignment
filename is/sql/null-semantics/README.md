# Null semantics

SQL has three truth values. A comparison with a null is unknown, `WHERE`
keeps only the rows that are true, and `NOT unknown` is unknown.

The truth tables have one asymmetry worth stating: `false AND unknown` is
false and `true OR unknown` is true, because in those two cases the answer no
longer depends on the unknown value. Everything else involving unknown stays
unknown.

## The law of the excluded middle does not hold

One row, value null. `WHERE value = 1` returns nothing. `WHERE value <> 1`
returns nothing. The table has one row, and it appears in neither result.
That is measured here, not argued.

`engine_agrees` checks the module's `and_` and `or_` against sqlite3 for all
nine combinations of true, false and null. `IS NULL` is the only operator
that tests for a null and returns a definite answer.
