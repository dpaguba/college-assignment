# Generators

A linear congruential generator multiplies, adds and takes a remainder, and
all of its quality is in the three constants.

| multiplier, increment, modulus 16 | period |
|---|---:|
| 5, 3 | 16, the full period |
| 3, 1 | 8 |
| 4, 0 | 1 |

The Hull and Dobell conditions predict which of these is full, and the module
checks the prediction against the measured period rather than trusting it.
The third row is the failure worth seeing: a generator that produces one
value forever still looks like arithmetic.

Determinism is the feature. A simulation study has to be repeatable, so the
same seed must give the same stream, and the module checks that too. What
looks like a weakness of pseudo random numbers is the property that makes a
comparison between two model variants possible at all.
