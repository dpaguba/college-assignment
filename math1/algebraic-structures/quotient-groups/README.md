# Quotient groups

Multiplying cosets by multiplying representatives works only when the answer
does not depend on which representatives are chosen. That independence is
exactly normality, and it fails visibly.

In the symmetric group on three points, take a subgroup of order two. Two
choices of representative for the same pair of cosets give products lying in
different cosets, so the operation is not defined at all. The module reports
that by checking every pair of representatives rather than by testing
normality and citing the theorem, so the two facts are established
separately and then compared.

## The quotient of the cyclic group

Z12 by its subgroup of order four is a group of order three, and it is
isomorphic to Z3. Both facts are computed: the quotient is constructed as a
group of cosets, its axioms are verified, and an isomorphism to Z3 is found
by search.

That is the pattern the ring chapter repeats with ideals, and the pattern the
homomorphism theorem completes: every quotient is the image of some
homomorphism, and every image is a quotient.
