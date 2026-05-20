# Homomorphisms

A monoid is a set with an associative operation and a unit; a homomorphism
turns the operation into the operation and the unit into the unit.

The length of a list is the standard example: the length of a concatenation
is the sum of the lengths, and the empty list has length zero. The module
checks both conditions over samples rather than citing the property.

Reversal is the near miss. It preserves the unit and it does not preserve the
operation, since reversing a concatenation gives the reversed parts in the
other order, so it is a homomorphism into the opposite monoid and not into
this one.

## Why the lecture spends a session on this

A fold is exactly a homomorphism out of the term algebra. That is what makes
a definition written as a fold inherit the laws of the algebra it maps into,
and it is why the two modules before this one are worth their space: the
shape of the data, the fold over it, and the structure of the target are the
same statement three times.
