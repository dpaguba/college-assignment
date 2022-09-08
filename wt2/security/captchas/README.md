# CAPTCHAs

Six characters from 36 gives 31.02 bits and 2.2 billion possibilities, so a
blind guesser needs about a billion attempts. That number is not the
interesting one.

## The solver that reads most of it

A program that reads four of the six characters reliably and guesses the rest
succeeds once in 1296 attempts. At a few attempts a second that is a solved
challenge every few minutes, from a puzzle whose nominal space is two
billion. The strength of the challenge is set by what the machine cannot
read, not by the size of the space.

## The other side

| difficulty | human success | machine success |
|---|---|---|
| easy | 0.95 | 0.90 |
| medium | 0.85 | 0.40 |
| hard | 0.55 | 0.05 |

The separation is largest in the middle. Making the challenge harder past
that point excludes humans faster than machines, which is the failure mode of
every distorted-text puzzle that became unreadable.

A pure image challenge excludes blind users, and an audio alternative is the
minimum. The alternatives that avoid the puzzle altogether: rate limiting, a
proof of work, behaviour analysis, and a field that a human never sees and
therefore never fills in.
