# Password storage

A record holds a fresh salt, a derived value and the iteration count. The
derivation is PBKDF2 with HMAC-SHA256 from the standard library and the
comparison is `hmac.compare_digest`, which does not reveal through its
running time how many bytes matched.

## What the salt buys

`dictionary_attack` runs a list of common passwords against a set of accounts,
half of which use one. Every match costs a full derivation per account,
because each record has its own salt: the attacker cannot compute the list
once and compare against everyone. Without a salt that work is done once for
the whole database.

## What the iterations buy

`work_factor` measures a single derivation at 1000 and at 100000 iterations.
For a login the difference is a moment nobody notices; for an attacker it
multiplies every one of billions of guesses. Raising the count as hardware
gets faster is the maintenance this design requires.

## Length against complexity

Four words drawn at random from a list of 7776 carry 51.7 bits. Eight mixed
characters would carry 52.6 bits **if chosen uniformly**, and chosen by a
person they carry roughly 30. The module returns all three numbers rather than
the comparison alone, because the interesting part is the gap between the
theoretical figure and what people actually produce.

Rules that force a pattern make this worse: everyone appends the same digit
and the same punctuation mark, and the entropy the rule was supposed to add
goes into a shape the attacker already knows.
