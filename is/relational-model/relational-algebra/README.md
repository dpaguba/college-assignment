# Relational algebra

Selection, projection, union, difference, cartesian product and rename are
enough; intersection, join and division are written with them. The module
keeps that structure visible: `intersection` is two differences, `theta_join`
is a selection over a product, and `natural_join` only exists separately
because it drops the duplicated join columns.

Every operator is checked against sqlite3 on the exercise's three tables. The
difference `S − R` gives `(1,3,x)` and `(4,3,y)`, matching `EXCEPT`; the union
matches `UNION`, the intersection `INTERSECT`, the product the row count of
`FROM r, s`, and the projection `SELECT DISTINCT`.

## Where the arity check earns its place

`union` and `difference` refuse relations of different arity. Without that
check a difference between a two-column and a three-column relation would
quietly return the whole left side, since no tuple can ever be equal. The
error is the point: union compatibility is a condition on the schemas, not a
detail of the implementation.
