# Block cipher modes

A block cipher encrypts one fixed-size group. How the groups are chained is a
separate decision, and it decides almost everything.

The toy cipher here is a keyed, invertible mixing step. It protects nothing
and it is enough to show what the modes do.

## Three modes

**Electronic code book** encrypts each block on its own. Equal plaintext
blocks become equal ciphertext blocks, so the pattern of the plaintext stays
visible. `pattern_leak` counts the distinct blocks under both modes on a
plaintext with repetitions.

**Cipher block chaining** mixes each block with the previous ciphertext
block before encrypting, so repetitions disappear. Encryption is sequential;
decryption is not.

**Counter mode** encrypts a counter and combines the result with the
plaintext, which turns the block cipher into a stream cipher. No padding is
needed and both directions run in parallel.

## Error propagation

Flipping one bit of one ciphertext block corrupts:

| mode | blocks corrupted |
|---|---|
| ecb | 1 |
| cbc | 2 |
| ctr | 1 |

The chaining costs one extra block because the previous ciphertext block
enters the decryption of the next.

## The rule counter mode inherits

A counter value must never repeat under one key. Two messages encrypted with
the same counter give the same key stream, and combining the ciphertexts
cancels it: the same failure as a reused one-time pad, in a mode that is
otherwise the most comfortable of the three.

None of the three authenticates. Confidentiality without integrity is what
the transport attacks module exploits, and the answer there is the same as
here: authenticated encryption.
