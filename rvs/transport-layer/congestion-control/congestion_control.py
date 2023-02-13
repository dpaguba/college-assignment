"""TCP congestion control: slow start, congestion avoidance, and the two losses.

The sender has no direct information about the network, so it probes: increase
the window until something is lost, then back off. The two phases differ in how
fast it probes.

**Slow start** doubles the window every round trip, which is exponential and is
called slow only because the alternative it replaced was to start at the
receiver's window. **Congestion avoidance** adds one segment per round trip
above the threshold, which is linear.

The two loss signals are treated differently, and the difference is the whole
of TCP Reno. Three duplicate acknowledgements mean packets are still getting
through, so the window is **halved**. A timeout means nothing is getting
through, so the window drops to **one**.
"""

from __future__ import annotations

import math


def run(rounds, threshold, triple_duplicate_at=None, timeout_at=None):
    """The window over a number of round trips, with optional loss events.

    Each entry records the window **at the start** of that round, so a loss in
    round `k` shows up in the entry for round `k+1`. That is what a measured
    trace looks like too: the sender learns about the loss a round trip after
    it happened, which is the whole reason congestion control is hard.
    """
    window = 1.0
    trace = []

    for index in range(rounds):
        trace.append({"round": index, "window": window, "threshold": threshold,
                      "phase": "slow start" if window < threshold
                      else "congestion avoidance"})

        if index == timeout_at:
            threshold = window / 2
            window = 1.0
            continue

        if index == triple_duplicate_at:
            threshold = window / 2
            window = window / 2
            continue

        if window < threshold:
            window *= 2
        else:
            window += 1

    return trace


def throughput(loss, rtt, mss):
    """The classic square root formula for average TCP throughput.

    Throughput is proportional to `1 / sqrt(loss)`, so a hundredfold reduction
    in loss buys a tenfold increase in rate. That relationship is why a link
    with a small persistent loss rate performs so much worse than its bandwidth
    suggests, and why loss over a wireless hop is disproportionately damaging.
    """
    return 1.22 * mss / (rtt * math.sqrt(loss))


def fairness(rates):
    """Jain's fairness index of a set of flow rates.

    One when every flow gets the same, `1/n` when one takes everything. The
    additive increase and multiplicative decrease rule converges towards
    fairness, which is a property of the rule rather than of any coordination
    between the senders.
    """
    total = sum(rates)
    squares = sum(rate ** 2 for rate in rates)
    return total ** 2 / (len(rates) * squares) if squares else 1.0


def additive_increase_multiplicative_decrease(rates, capacity, steps):
    """Two flows sharing a link, converging towards an equal split.

    Each flow adds a constant while there is room and multiplies by a constant
    when there is not. The additive step moves the pair along a diagonal and
    the multiplicative step moves it towards the origin, so the sequence
    spirals onto the fair line. Additive decrease would not.
    """
    current = list(rates)
    history = [list(current)]

    for _ in range(steps):
        if sum(current) < capacity:
            current = [rate + 1 for rate in current]
        else:
            current = [rate / 2 for rate in current]
        history.append(list(current))

    return history
