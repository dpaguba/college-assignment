# Aggregation

`GROUP BY` folds rows into groups, `WHERE` filters rows before that happens
and `HAVING` filters groups after. The three parties in the example give
three groups; requiring more than one member leaves two.

## Nulls change the counts

On a column with three values and two nulls, `COUNT(*)` returns 5 and
`COUNT(value)` returns 3: the star counts rows, the column counts values.
`AVG(value)` returns 20.0, the mean of 10, 20 and 30. Replacing the nulls by
zero with `COALESCE` returns 12.0. Both are reasonable answers to different
questions, and SQL picks the first one: an aggregate skips the nulls rather
than treating them as a number.

`is_ambiguous` is a small linter for the other classic mistake, a bare column
next to an aggregate without being grouped. sqlite3 accepts that query and
picks an arbitrary row; the standard rejects it, and so does this function.
