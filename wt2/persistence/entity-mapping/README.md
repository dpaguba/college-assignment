# Entity mapping

An entity is a row with an identity. Equality follows the key, not the
fields: the same row read twice and edited once is still the same row, and a
set that holds both must hold one element, not two. The module measures that
difference, and the field-based comparison gives 2 where the key-based gives
1.

The awkward case is the new object. Before the insert, a generated key is not
known, so there is nothing to compare and identity falls back to object
identity. That is the reason a generated key makes a poor basis for `hashCode`
in a collection that outlives the insert.

Key strategies: identity (the database counts, known only afterwards),
sequence (readable in advance, so a batch can be prepared), table (portable
and slow), assigned (the application knows the key already).

Without configuration the table name follows the class name and every field
becomes a column; a transient field is one that is deliberately left out.
