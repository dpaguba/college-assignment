# Reliable transfer

Three protocols, differing in how much is in flight and what a loss costs.

## Stop and wait is unusable, and the number says why

On a link with a 30 ms round trip and a frame that takes 8 microseconds to
transmit, the sender is busy 0.0003 of the time. The window multiplies that
directly:

| window | utilisation |
|---|---|
| 1 | 0.0003 |
| 100 | 0.027 |
| 1000 | 0.267 |

The right window is the bandwidth-delay product: a 1 Gbit/s link with a 30 ms
round trip holds **3.75 MB**, and anything smaller leaves the link idle
however fast the endpoints are.

## Go back N against selective repeat

Sending ten packets with a window of four:

| loss at | go back N | selective repeat |
|---|---|---|
| packet 0 | **14** transmissions | **11** |
| packet 3 | 11 | 11 |

The second row is the one worth noticing: when the loss is the last packet of a
window, the two protocols cost the same. Go-back-N's penalty is not the loss,
it is everything sent **after** the loss that the receiver discarded.

## The window bound is not the same for the two

Go-back-N may use `2^k - 1` sequence numbers, selective repeat only `2^(k-1)`,
because its receiver accepts a range and a retransmission must not look like a
new packet. Getting that wrong yields a protocol that passes testing and
duplicates data under loss.
