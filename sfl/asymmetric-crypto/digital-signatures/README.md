# Digital signatures

The same computation as encryption with the roles of the keys exchanged:
sign with the private key, verify with the public one. A changed message
fails verification, which the module checks on the exercise key.

## Why the hash comes first

Three reasons, and only the first is about size. A message can be longer than
the modulus and could not be signed at all. The hash has a fixed length, so
the signature stays one block whatever the message. And the hash removes the
arithmetic structure that raw RSA carries.

That third reason is the interesting one. `malleability` signs 5 and 7, then
multiplies the two signatures and obtains a valid signature for 35, without
the private key. RSA is multiplicative: the signature of a product is the
product of the signatures. Signing the hash instead breaks the connection,
because the product of two hashes is not the hash of anything in particular.

## What a signature is and is not

It gives authenticity, integrity and non-repudiation. It gives no
confidentiality at all: the message sits in the clear beside it.

Against a message authentication code: a code needs a shared key, so either
party could have produced it and neither can prove anything to a third. A
signature needs no shared secret and is verifiable by anyone, at the cost of
being far slower.
