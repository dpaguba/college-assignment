# Subqueries

A subquery in `WHERE` runs once if it is independent of the outer row and
once per row if it refers to it. `correlated` looks for an alias of the outer
query inside the parentheses to tell the two apart.

## NOT IN against a list with a null

Values 1, 2, 3 on the left, 2 and a null on the right.
`WHERE value NOT IN (SELECT value FROM right_side)` returns nothing at all.
The comparison `1 <> NULL` is unknown, so `1 NOT IN (2, NULL)` is unknown,
and an unknown row does not pass `WHERE`.

`WHERE NOT EXISTS (…)` on the same data returns 2 rows, because it asks
whether a matching row was found, and no comparison with the null ever has to
produce a truth value.

This is the most common way the three-valued logic bites in practice, and the
fix is either `NOT EXISTS` or an explicit `IS NOT NULL` inside the subquery.
An uncorrelated `IN` subquery rewrites to a join; the module checks that both
return the same 2 rows here.
