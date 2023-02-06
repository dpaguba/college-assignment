"""Medium access: who may transmit, and what a collision costs.

With one shared medium, two transmissions at once destroy each other. The
protocols differ in how much they look before sending and what they do
afterwards.

| protocol | peak throughput |
|---|---|
| pure ALOHA | **18.4%** |
| slotted ALOHA | **36.8%** |
| CSMA/CD | approaches 1 on a short link |

The ALOHA numbers are the famous ones and they come out of one calculation: a
frame survives if no other frame starts in a vulnerable period, which is two
frame times for pure ALOHA and one for the slotted version. Halving the
vulnerable period doubles the throughput exactly.
"""

from __future__ import annotations

import math


def aloha_throughput(load, slotted):
    """Successful transmissions per frame time, at a given offered load.

    `G e^(-2G)` for pure ALOHA and `G e^(-G)` for the slotted version. Both
    peak and then fall: beyond the peak, more offered traffic means fewer
    successful frames, which is congestion collapse in its simplest form.
    """
    if slotted:
        return load * math.exp(-load)
    return load * math.exp(-2 * load)


def aloha_peak(slotted):
    """The best throughput and the load that achieves it."""
    if slotted:
        return {"load": 1.0, "throughput": 1 / math.e}
    return {"load": 0.5, "throughput": 1 / (2 * math.e)}


def csma_efficiency(stations, propagation, transmit):
    """Efficiency of CSMA/CD, as a function of the propagation delay.

    The standard approximation is `1 / (1 + 5a)` where `a` is the propagation
    delay divided by the transmission time. A short cable and long frames make
    `a` small and the efficiency near one; a long cable makes collisions
    expensive because a station learns about them late.

    That single ratio is why Ethernet's maximum segment length and minimum
    frame size are tied together.
    """
    ratio = propagation / transmit
    return 1.0 / (1.0 + 5 * ratio)


def minimum_frame_bits(rate, propagation):
    """The smallest frame that guarantees a collision is heard while sending.

    A station must still be transmitting when a collision from the far end
    reaches it, so the frame must take at least a round trip. At 10 Mbit/s with
    a 25.6 microsecond one-way delay that is 512 bits, which is exactly
    Ethernet's 64-byte minimum.
    """
    return int(rate * 2 * propagation)


def backoff_range(collisions):
    """The size of the window a station picks its backoff from.

    Doubles per collision and stops at 1024, which is what "binary exponential"
    and "truncated" mean. Doubling makes the protocol stable under load;
    truncating stops the delay from growing without bound when the network is
    simply broken.
    """
    return 2 ** min(collisions, 10)


def expected_backoff(collisions, slot_time):
    """The average wait after a number of collisions."""
    return (backoff_range(collisions) - 1) / 2 * slot_time


def hidden_terminal(distance_ab, distance_bc, distance_ac, range_):
    """Whether two stations cannot hear each other but share a receiver.

    A and C are both in range of B and out of range of each other, so neither
    detects the other's transmission and both collide at B. Carrier sense is
    useless here, which is why wireless uses request-to-send and clear-to-send
    instead of collision detection.
    """
    return (distance_ab <= range_ and distance_bc <= range_
            and distance_ac > range_)
