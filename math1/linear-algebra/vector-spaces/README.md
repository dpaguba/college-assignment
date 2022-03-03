# Vector spaces

Span, independence, basis, dimension. All four reduce to the rank of a
matrix, which is why the module is short: a family is independent when its
rank equals its size, a vector lies in the span when adding it leaves the
rank unchanged, and the dimension is the rank.

## The exchange lemma is what makes dimension meaningful

Steinitz: a vector in the span of a family can replace one of its members
without changing the span. Repeating the exchange turns any independent
family into part of any spanning one, and the consequence is that two bases
of the same space have the same size. Without it, "the dimension" would be a
property of a chosen basis rather than of the space.

The module performs the exchange explicitly, searching for a member that can
be dropped, so the lemma is a computation with a witness rather than an
existence claim.

## Coordinates

Writing a vector in a basis is solving a linear system, and uniqueness of the
solution is uniqueness of the representation. That is the whole content of
"a basis gives coordinates", and it is why the next module about elimination
comes before the one about linear maps: coordinates are needed to write a map
down at all.
