# Unification

Making two types equal with the least commitment possible. The result is a
most general unifier: any other solution is an instance of it, which is what
makes inference produce one answer rather than a family of them.

The occurs check is the part that cannot be skipped. Unifying `a` with
`a -> int` succeeds without it and produces an infinite type, and the type
checker then loops rather than reporting an error. The module checks that
such a unification returns nothing.

Two structures unify componentwise, a variable binds to anything that does
not contain it, and two different constants never unify. Those three cases
are the whole algorithm, and everything the type inference does is built on
them.
