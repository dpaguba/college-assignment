# Hashing, MACs and certificates

A hash maps any input to a fixed digest, deterministically, with an unrelated
result for a changed input. The avalanche property is measurable: two inputs
differing in one character produce digests differing in roughly half their
bits.

## The birthday bound halves the security

A collision takes about `2^(n/2)` attempts, not `2^n`. A 64-bit digest falls to
`2^32` work, which is seconds, and that is why every modern hash is at least
256 bits. Finding a **specific** preimage still takes `2^n`, so the two
properties have very different costs and are worth naming separately.

## Three levels of assurance

| primitive | proves | to whom |
|---|---|---|
| hash | the message is unchanged | anyone who has the right digest |
| MAC | the message came from a holder of the key | the other key holder |
| signature | the same | **anyone**, using the public key |

The third row is the one that needs asymmetric cryptography. A MAC cannot prove
anything to a third party, because either key holder could have produced it.

## Comparing tags in constant time

A byte-by-byte comparison that returns early leaks how many bytes matched, and
an attacker recovers a tag one byte at a time by timing it. That is a real
attack on real systems and the fix is one function call, which is why
`compare_digest` exists at all.

## A certificate is a signed binding

It binds a name to a key so that a verifier who trusts the authority need not
have met the subject. Altering the key invalidates the signature, verified
directly. The flip side is that a compromised authority makes every binding it
ever issued worthless, which is the structural weakness of the whole system.
