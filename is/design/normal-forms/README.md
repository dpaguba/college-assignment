# Normal forms

Each form forbids one shape of dependency. The first forbids a value that is
itself a collection. The second forbids a non-key attribute that already
depends on part of a key. The third forbids one that depends on another
non-key attribute. Boyce-Codd drops the exception the third makes for key
attributes and demands that every non-trivial left side be a superkey.

The classic separating example is student, subject, teacher with
`{student, subject} → teacher` and `teacher → subject`. It is in third normal
form, because `subject` is a key attribute, and it is not in Boyce-Codd,
because `teacher` is not a superkey. The tests check exactly that pair of
answers.

## What normalisation buys

The three anomalies are insert, update and delete. A schema that stores a
fact twice can be changed in one place and not the other; a schema that can
only store a fact as part of another one loses it when that other is deleted.
Higher normal forms remove the redundancy that makes those possible, and the
price is a join at query time.
