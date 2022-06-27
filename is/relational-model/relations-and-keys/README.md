# Relations and keys

A relation is a set of tuples over a fixed schema, so the constructor drops
duplicates and the order of the rows carries nothing. Everything else in the
model follows from that: a key is a set of attributes whose projection stays
as large as the relation, a minimal key is one that loses that property when
any attribute is removed.

`candidate_keys` searches upwards by size and skips every set that contains a
key already found. On the three-row relation `(1,1,1), (1,2,2), (2,1,3)` it
returns `c` and `a b`: the single attribute `c` separates the rows, and `a`
and `b` need each other.

## What the constraints actually forbid

Entity integrity forbids a null inside a key, because a key that is unknown
cannot identify anything. Referential integrity forbids a foreign-key value
with no matching row, but it permits a null there, which is a different
statement: the null means no reference exists at all, not an unknown one that
might be wrong.

A key of an instance is not a key of the schema. The functions here answer
the question about the rows in front of them; whether a key holds for every
possible instance is a question for the functional dependencies.
