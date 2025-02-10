# One-time pad

Combine the message with a key of the same length, bit by bit. Encryption and
decryption are the same operation, because the exclusive or is its own
inverse.

## What perfect means

For every ciphertext and every candidate plaintext of that length there is
exactly one key that connects them. `perfect_secrecy` enumerates them: the
number of plaintexts still possible equals the number of all plaintexts of
that length. The ciphertext rules nothing out, no matter how much
computation an attacker has. That is a stronger statement than any other
cipher can make, and it is the only one that has been proved.

The conditions are four: the key is truly random, at least as long as the
message, used exactly once, and exchanged over a secure channel. The last one
is why it is rarely used: a channel able to carry the key securely could have
carried the message.

## Two ways to lose it

Reusing a key destroys everything. Combining the two ciphertexts cancels the
key and leaves the two plaintexts combined with each other, which is a
puzzle that language statistics solve. `key_reuse` returns both combinations
so they can be seen to be identical.

Deriving the key from a 256-bit seed is not a pad. Whatever the message
length, there are only 2²⁵⁶ possible key streams, and the security rests on
the generator. What that describes is a stream cipher, which is a reasonable
thing to build and a different claim to make.

## Exercise 5.3c

Seven intercepted messages, each with its own pad, so no content is readable.
The lengths are not equal: 16 bits for four of them and 14 for three. Knowing
that exam 007 is one's own and that it passed identifies 16 bits as passed
and 14 as failed, and with it every other student's result:

| exam | bits | outcome |
|---|---|---|
| 001 | 16 | passed |
| 002 | 14 | failed |
| 003 | 14 | failed |
| 004 | 16 | passed |
| 005 | 16 | passed |
| 006 | 14 | failed |
| 007 | 16 | passed |

A perfect cipher hides the content and not the length. Padding every
plaintext to the same length closes it, which `exam_results(padded=True)`
shows by returning no classification at all.
