# Key exchange

## Diffie-Hellman

Each side picks a secret exponent, sends the generator raised to it, and
raises what arrives to its own secret. Both reach the same power. With p = 23,
g = 5 and secrets 6 and 15, the values 23, 5, 8 and 19 travel and the shared
key is not among them.

The security rests on the discrete logarithm: from `g^a mod p` there is no
known way back to `a`.

## Merkle's puzzles, compared

Exercise 6.4 asks what the two constructions rest on. Merkle's puzzles rest
on nothing but effort. One side sends many weakly encrypted puzzles, the
other solves one and names its identifier; an eavesdropper does not know
which and must solve about half of them. With n puzzles the legitimate work
is n and the attacker's is n², a quadratic gap.

That gap is real and too small. Doubling the attacker's cost needs four times
the legitimate work, so the construction cannot be scaled to a useful
margin.
Diffie-Hellman gets an exponential gap from a hard problem instead of from
bookkeeping, and that is the difference the exercise is pointing at.

## The middle

An unauthenticated exchange has no answer to the question of whose power just
arrived. `man_in_the_middle` runs two exchanges, one with each side, and both
sides end up sharing a key with the attacker while believing they share one
with each other. The arithmetic is correct throughout; what is missing is
authentication.

Signing the public values closes it, which shifts the problem to knowing the
right public key, and that is what the certificate infrastructure is for.

Ephemeral secrets buy forward secrecy: a long-term key stolen later does not
open recorded sessions, because the session keys were never derived from it.
