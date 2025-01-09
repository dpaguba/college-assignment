# Hash functions

Four criteria: compression, preimage resistance, second preimage resistance,
collision resistance. Exercise 6.3a offers three candidates and asks which
are hash functions and how good.

| candidate | compression | preimage | second preimage | collision |
|---|---|---|---|---|
| H₁ = last block | yes | no | no | no |
| H₂ = sum of blocks | yes | no | no | no |
| H₃ = G(G(M)) | yes | yes | yes | yes |

For H₁ no search is needed: a preimage of h is any message ending in h, and
prefixing anything to a message leaves the hash alone. `preimage_of_last_block`
writes one down directly, which is the published reasoning.

For H₂ addition is commutative, so any reordering collides;
`collision_for_sum` returns `[1, 2, 3]` and `[3, 2, 1]`.

H₃ inherits everything from G, because a collision of the composition
contains a collision of G. The one condition is that G must accept its own
output as input.

## Exercise 6.3d

A hash with a deterministic inverse, 512 bits in and 160 bits out. It is
plainly not preimage resistant. Can it still resist collisions?

No, and the work is two evaluations. Hash any message, hand the result to the
inverse, and take what comes back. Each hash value has about 2³⁵² preimages,
so the returned message is a different one with probability 1 − 2⁻³⁵², and a
different message with the same hash is a collision. The birthday bound of
2⁸⁰ is what an attacker would need *without* the inverse; with it the cost
collapses to constant.

## MD5 and SHA-256

128 bits against 256, birthday bounds of 2⁶⁴ against 2¹²⁸, and collisions for
the first have been published for years. That is exercise 6.3b: two files of
the same size with different contents and the same MD5, and different SHA-256
values. A function can still compress perfectly well and be useless where
integrity is the point.
