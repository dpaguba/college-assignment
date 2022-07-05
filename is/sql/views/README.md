# Views

A view stores a query, not a result. The view over presidents with a term
above two has 3 rows; after inserting a fourth such president it has 4,
without any refresh, because the query is re-evaluated each time.

## When a view can be written to

An update to a view has to translate into an update of the base tables, and
that translation has to be unique. A view with a group by, an aggregate, a
`DISTINCT`, a union or more than one table gives no unique answer, so
`is_updatable` rejects those and accepts a plain projection with a selection.

A materialised view stores the result instead: faster to read, needs storage,
and can be stale until it is refreshed. That is the same trade as an index,
made at the level of whole queries.

Views are used for three things: hiding a complicated query behind a name,
restricting what a user can see, and keeping applications working when the
tables underneath change.
