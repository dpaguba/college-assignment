# Modular arithmetic

The three identities of exercise 6.1, checked by computation rather than
argued.

1. `a^b mod n = (a mod n)^b mod n` holds without conditions: reducing the
   base first changes nothing.
2. `(a^b mod n) mod n = a^b mod n` holds trivially: a second reduction does
   nothing.
3. `a^b mod n = a^(b mod φ(n)) mod n` for `n = pq` holds **only when a and n
   are coprime**. Euler's theorem gives `a^φ(n) ≡ 1` exactly then, and the
   exponent may be reduced. `identity_three_report` searches for a
   counterexample among the non-coprime cases and finds one, so the identity
   is confirmed under its condition and refuted without it.

That third line is the one the exercise is testing: the hint names Euler's
theorem, and the theorem carries a hypothesis that is easy to drop.

## The tools

`totient` counts the coprimes directly, which is slow and unambiguous.
`extended_euclid` yields the modular inverse, and `inverse(13, 60)` gives 37,
the value the RSA exercise asks for. Without coprimality there is no inverse
and the function raises rather than returning something.

`power` squares repeatedly, so the work grows with the number of digits of
the exponent instead of its value; `power_slow` multiplies step by step and
exists to check it. `exponentiation_agrees` compares them across bases,
exponents and moduli.

Both hard problems behind the public-key schemes are named at the end:
factoring and the discrete logarithm. Neither is proved hard. What is known
is that nobody has published a fast method, which is a weaker statement than
it is usually taken for.
