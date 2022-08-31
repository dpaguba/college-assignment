# Relationships

A 1:n relationship puts a foreign key on the many side. An n:m relationship
has nowhere to put one and needs its own table.

## One side owns it

A bidirectional relationship is two references in memory and one column in
the database. The side with the column owns the relationship; the other
declares itself mapped by it and writes nothing.

Setting only the inverse side is the classic mistake: the collection in
memory is correct, the column stays empty, zero row changes are written, and
after a reload the relationship is gone. The module counts exactly that: one
reference in memory, no rows written.

## Cascades

Deleting an author with the cascade removes the books; without it the books
stay and point at an author that no longer exists. Orphan removal is a
different rule: it fires when a child is taken out of the collection, not
only when the parent is deleted.
