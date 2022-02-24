# Semigroups and monoids

One operation, and the conditions added one at a time: closure gives a magma,
associativity a semigroup, an identity a monoid, inverses a group.

How much associativity costs:

| set size | operations | associative |
|---|---:|---:|
| 2 | 16 | 8 |
| 3 | 19 683 | 113 |

Half of the operations on two elements are associative and about half a
percent of those on three. The condition is far more restrictive than it
looks when written as one line, and the drop is the reason semigroups are a
subject rather than a remark.

## The identity is unique when it exists

If two identities existed, each would leave the other unchanged, so they
would be equal. The module returns a list and the list never has two entries,
which is the computational form of that one-line argument.

Subtraction modulo n is the standard non-example: closed, with a right
identity, and not associative, which the check finds immediately.
