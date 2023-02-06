# Medium access

With one shared medium, two transmissions at once destroy each other.

| protocol | peak throughput |
|---|---|
| pure ALOHA | **0.1839** at load 0.5 |
| slotted ALOHA | **0.3679** at load 1.0 |
| CSMA/CD, short link | 0.95 |

The ALOHA numbers come out of one calculation: a frame survives if nothing else
starts within its vulnerable period, which is two frame times unslotted and one
slotted. Halving the vulnerable period doubles the throughput exactly, which is
what the pair of numbers shows.

Both curves peak and then **fall**: past the peak, more offered traffic means
fewer successful frames. That is congestion collapse in its simplest form.

## Why Ethernet frames have a minimum size

A station must still be transmitting when a collision from the far end reaches
it, so a frame must take at least a round trip. At 10 Mbit/s with a 25.6
microsecond one-way delay that is **512 bits**, which is exactly the 64-byte
minimum in the standard. The maximum cable length and the minimum frame size
are the same constraint written twice.

## Backoff

The window doubles per collision and stops at 1024. Doubling makes the protocol
stable under load; truncating stops the delay growing without bound when the
network is simply broken.

## Where carrier sense stops working

Two stations in range of a receiver and out of range of each other both send
and collide at the receiver, and neither can detect it. That is the hidden
terminal problem, and it is why wireless replaces collision detection with a
request-to-send exchange.
