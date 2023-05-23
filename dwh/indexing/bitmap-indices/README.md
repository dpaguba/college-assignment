# Bitmap indices

One bitmap per distinct value, one bit per row. A predicate is a lookup, a
disjunction is a bitwise or, and a conjunction across columns is a bitwise
and, which is exactly the shape a star join needs.

The size is rows times distinct values, so the index is small for a column
with five values and larger than the table for one with a million. That is
the whole rule for when to use it: low cardinality, which in a warehouse
means most dimension attributes.

The bitmaps of one column partition the rows, since every row has exactly one
value, and the module checks that: the columnwise sums are all one. A
partition is what lets a negation be computed as a complement rather than as
a scan.
