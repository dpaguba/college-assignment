# RSA

## Exercise 6.2a

With p = 7, q = 11 and e = 13: n = 77 and φ(n) = 60. The private exponent is
the inverse of 13 modulo 60, so 13·d ≡ 1 (mod 60), giving **d = 37**, since
13·37 = 481 = 8·60 + 1. That is the published answer, and the module computes
it with the extended Euclidean algorithm rather than by trial.

`roundtrip_holds` checks every message from 0 to 76, not a sample. It works
for all of them, including those sharing a factor with n, because n is a
product of distinct primes and the Chinese remainder theorem covers those
cases too.

## Exercise 6.2b: knowing φ(n) is knowing the factors

From φ(n) = (p − 1)(q − 1) = n − p − q + 1 follows p + q = n + 1 − φ(n). With
the sum and the product, p and q are the roots of a quadratic. `factor_from_phi`
solves it in integers and refuses anything that does not come out whole, and
it recovers 7 and 11 from (77, 60) and 53 and 61 from (3233, 3120).

The consequence is a statement about what must be kept: φ(n) is not a
harmless intermediate value, it is the private key in another form.

## Exercise 6.2c: why the padding

Without padding, encryption is a function of the message alone. An attacker
who knows the recipient's public key and guesses the plaintext encrypts the
guess and compares. A match confirms it. `deterministic_without_padding`
returns two ciphertexts of the same message that are identical without
padding and different with it.

A small exponent makes it worse. With e = 3 and a small message, m³ stays
below the modulus, so no reduction happens at all and the integer cube root
returns the message. The private key never enters the picture.
