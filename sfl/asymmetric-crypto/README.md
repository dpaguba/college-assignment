# Asymmetric cryptography

Five modules following exercise 6: the modular arithmetic underneath, RSA,
hash functions, signatures and key exchange.

Three published answers are reproduced exactly: d = 37 for p = 7, q = 11 and
e = 13; the derivation of p and q from n and φ(n) through p + q = n + 1 − φ(n);
and the rating of the three candidate hash functions.

One answer is sharper than expected. Exercise 6.3d asks whether a hash with a
deterministic inverse can still resist collisions. It cannot, and not because
of the birthday bound: hashing any message and asking the inverse for a
preimage produces a collision in two evaluations, since a 512-bit input space
mapped to 160 bits gives every hash about 2³⁵² preimages.

The recurring lesson is that the secret is larger than it looks. φ(n) is the
private key in another form; the multiplicative structure of raw RSA is
enough to forge a signature; and a deterministic encryption confirms a guess
for anyone holding the public key.
