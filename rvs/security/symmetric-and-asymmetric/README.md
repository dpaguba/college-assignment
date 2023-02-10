# Symmetric and asymmetric cryptography

One key or a pair, and the trade is exact.

| | keys for 10 parties | speed |
|---|---|---|
| symmetric | **45** | fast |
| asymmetric | **20** | orders of magnitude slower |

The quadratic key count is the distribution problem, and it is what public key
cryptography solves. The speed is why it is never used alone.

## Hybrid encryption is what everything actually does

A fresh symmetric key encrypts the message, and the public key encrypts the
symmetric key. The expensive operation runs once on a few bytes instead of on
the whole message, which is the only way it is affordable, and it is what every
TLS handshake performs.

## One algorithm, two uses

Encrypting with the private key produces something only the public key undoes,
which is not a secret but a **signature**. That symmetry is why RSA gives both
confidentiality and authenticity, and it is verified here directly: a value
raised to the private exponent comes back through the public one.

## What this implementation is not

The RSA here uses 16-bit primes and no padding, so it demonstrates the
arithmetic and nothing else. The symmetric cipher is exclusive or with a
repeating key, which round-trips and leaks the exclusive or of any two messages
sent under the same key. Both are teaching models, and both would be a
catastrophe in use.
