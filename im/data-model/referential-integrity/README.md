# Referential integrity

A table can only be created once everything it references exists, which makes
the creation order a topological sort of the reference graph. It is not
unique: the four tables without references may come in any order. Dropping
reverses it.

`orphans` finds foreign keys whose target is missing, which is the state a
database gets into when the constraint was never declared or the data came
from a predecessor system that did not know the rule.

## The three answers to a delete

RESTRICT refuses the delete while references remain. CASCADE deletes the
referencing rows too. SET NULL leaves them and empties the reference. Which
one is right depends on a single question: does the referencing row still
make sense without its target? A receipt position without its receipt does
not. A receipt without its seller does.

## The trap in the environment

In sqlite the foreign key check is off by default, for historical reasons,
and has to be switched on **per connection** with `PRAGMA foreign_keys = ON`.
Forgetting it gives a database that accepts orphaned references without a
word, and the symptom appears much later: a join returns fewer rows than
expected.
