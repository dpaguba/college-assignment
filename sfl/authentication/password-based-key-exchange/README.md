# Password-based key exchange

The subject of the Boyd and Mathuria chapter that came with the course. Two
sides share a password, which is short and guessable, and want a session key,
which must not be.

The construction here follows SPEKE: the generator of the group is derived
from the password, and a Diffie-Hellman exchange runs over it. Two sides with
the same password derive the same generator and reach the same key. Two sides
with different passwords use different generators and reach different keys.
The password itself never travels.

## Why not simply send the hash

`naive_scheme` shows the two failures of the obvious approach. The value the
server checks is exactly the value that travelled, so an eavesdropper replays
it without knowing the password. And the recorded value can be run against a
dictionary offline, as often as the attacker likes, with the server none the
wiser.

## What a proper scheme achieves

Nothing on the wire lets a guess be tested. An attacker who wants to try
passwords must try them against the server, one connection per guess, where
they can be counted and slowed down. Online guessing remains possible and is
a problem with a known answer; offline guessing is the one that had to be
removed.

Compared to sending the password over an encrypted connection: there the
server receives the password itself and has to handle it correctly. Here it
never sees it. The certificate is still needed, to know that the server on
the other end is the intended one.
