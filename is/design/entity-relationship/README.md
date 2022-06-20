# Entity-relationship modelling

The exercise's model has courses that require other courses and teachers who
look after them. Both sides of "requires" are `(0, *)`: a course may require
nothing and may be required by nothing. The teaching relationship is
`(1, *)` on the course side, so every course has someone responsible.

## Mapping to tables

An n:m relationship needs its own table, because neither side can hold the
other's key. A 1:n relationship does not: the key of the one side becomes a
foreign key on the many side, and the relationship disappears as a separate
object. A weak entity has no key of its own and takes its owner's, which is
why deleting the owner deletes it.

The mapping loses the distinction between a relationship and an entity. Two
schemas that look identical can come from different diagrams, and that is why
the diagram is kept: it records an intention the tables no longer show.
