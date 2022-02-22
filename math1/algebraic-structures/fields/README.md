# Fields

A commutative ring where every non-zero element is invertible. The residues
modulo n are a field exactly for prime n, checked for every n below 30, and
the failure is always the same: a composite modulus has zero divisors, and a
zero divisor cannot be invertible.

## What "exactly when n is prime" does not say

It says nothing about which sizes a field may have. There is a field with
four elements, and it is not Z/4. It is the polynomials over the two-element
field modulo an irreducible quadratic, and its characteristic is 2 rather
than 4, because adding the one to itself twice already gives zero.

| | Z/4 | GF(4) |
|---|---|---|
| a field | no | yes |
| characteristic | 4 | 2 |

That is the first place in the course where the size of a structure and the
arithmetic inside it come apart, and it is the reason finite fields are
classified by prime powers rather than by primes.

## The multiplicative group

The non-zero elements of a finite field form a cyclic group, verified here
for every prime modulus up to 13 by finding a generator. That single fact is
what discrete logarithm cryptography rests on, and what makes primitive roots
worth naming.
