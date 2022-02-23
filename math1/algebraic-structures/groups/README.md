# Groups

A monoid in which everything is invertible, and that one condition carries
the whole theory: it gives cancellation, makes every row of the Cayley table a
permutation, and forces the order of every element to divide the order of the
group.

The groups of order eight, classified by searching every bijection for being
a homomorphism:

| | abelian |
|---|---|
| Z8 | yes |
| Z4 × Z2 | yes |
| Z2 × Z2 × Z2 | yes |
| D4, the square's symmetries | no |
| Q8, the quaternions | no |

Five classes, which is the known answer, and the search is what makes it a
result here: two groups are declared different only after every one of the
8! bijections has failed to be a homomorphism.

## Where groups come from

Addition modulo n is a group. Multiplication modulo n is not, since zero has
no inverse and neither does any element sharing a factor with the modulus.
Restricting to the units repairs it, and the units modulo 12 form a group of
order four that is not cyclic, which is the smallest example of a unit group
that is not.

The symmetric group is the other source. It is abelian on two points and not
on three, and the failure at three points is the reason almost every
interesting group is non-abelian.
