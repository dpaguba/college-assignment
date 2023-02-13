# Congestion control

The sender has no direct information about the network, so it probes: increase
until something is lost, then back off.

**Slow start** doubles the window per round trip and is called slow only
relative to what it replaced. **Congestion avoidance** adds one segment per
round trip above the threshold.

## The two losses mean different things

| signal | window becomes | reasoning |
|---|---|---|
| three duplicate acknowledgements | **half** | packets are still arriving |
| timeout | **one** | nothing is arriving |

Both set the threshold to half the window. The distinction is the whole of TCP
Reno, and the trace shows the effect one round after the event, which is also
when a real sender learns about it.

## Throughput falls with the square root of loss

At a 100 ms round trip and 1500-byte segments:

| loss rate | throughput |
|---|---|
| 1e-2 | 0.18 Mbit/s |
| 1e-3 | 0.58 |
| 1e-4 | 1.83 |
| 1e-5 | **5.79** |

A hundredfold reduction in loss buys a tenfold increase in rate. That is why a
link with a small persistent loss performs so far below its bandwidth, and why
loss over a wireless hop, which is not congestion at all, is so damaging.

## Fairness is a property of the rule

Additive increase with multiplicative decrease converges to an equal split
without any coordination between senders. Additive decrease would not: the
multiplicative step is what moves the pair towards the diagonal rather than
along it.
