# Security

| Topic | |
|---|---|
| [symmetric-and-asymmetric](symmetric-and-asymmetric/) | one key or a pair, and why both |
| [hashing-and-signatures](hashing-and-signatures/) | integrity, authenticity, and who can check it |

Two modules and one theme: every primitive here answers a different question,
and using the wrong one gives an answer that looks right. Encryption is not
integrity, a hash is not a MAC, and a MAC is not a signature, because each
proves something to a different audience.
