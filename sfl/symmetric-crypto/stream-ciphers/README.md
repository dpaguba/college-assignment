# Stream ciphers

A generator produces a key stream and the stream is combined with the
plaintext. The construction is a one-time pad with the randomness replaced by
a generator, and everything depends on how good that replacement is.

## A linear generator is not one

The generator here is linear on purpose. Three consecutive outputs determine
its parameters, so an attacker who knows a piece of plaintext computes the
stream at that position, recovers the parameters and generates the rest.
`linear_generator_is_broken` does exactly that and reports how many values it
needed and how many it then predicted.

The period is the second limit: once the stream repeats, the cipher is
reusing a pad. `period` measures it by following the state until it returns,
and for the parameters of the exercise it is the full modulus.

## No integrity at all

The ciphertext is the plaintext with the stream laid on top. Flipping a bit
of the ciphertext flips the same bit of the plaintext, without the key.
`bit_flipping` changes "transfer 10 euro" into "transfer 90 euro" by flipping
one byte, and nothing notices.

With a message authentication code over the ciphertext the change is
detected. That is not an optional extra: a stream cipher without one is a
cipher an attacker can edit.

The rules that follow: never repeat a key stream, use a generator whose
output does not reveal its state, add a tag, and make the nonce part of the
state rather than only the key.
