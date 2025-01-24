# Onion routing

Exercise 7.4 asks how anonymity is achieved, what each node knows, what one
or several controlled nodes can do, and how deanonymisation could happen.

The sender arranges a key with each of three nodes and wraps the message once
per node, innermost layer for the last node. Each node removes exactly its
own layer and forwards. `wrap` and `peel` model that, and after three peels
the payload is back.

## What each node knows

| node | knows the sender | knows the destination |
|---|---|---|
| entry | yes | no |
| middle | no | no |
| exit | no | yes |

The entry knows who is speaking because the packets come from them, and not
to whom, because that is under two more layers. The exit knows the
destination because it delivers there, and not the sender. The middle knows
only its two neighbours, which is exactly the point of having it.

## One node against two

A single controlled node sees one end. It can read the traffic if it is the
exit, and it can delay or drop, but it cannot connect a sender to a
destination. Controlling the entry and the exit of the same circuit does
connect them, through the timing and the sizes of the packets. With a share p
of the network the chance of holding both ends is about p².

## Two things it does not do

The exit sees exactly what a network operator would see without onion
routing. If the connection to the site is not encrypted, it reads along.
Anonymity is not confidentiality.

And traffic analysis needs no node at all. An observer who can watch both
ends matches the timing and the sizes without touching the encryption. The
assumption the whole design rests on is that the attacker sees only part of
the network; padding, cover traffic and delays would weaken that requirement
and cost bandwidth and latency that users notice.
