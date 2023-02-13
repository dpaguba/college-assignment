"""Reliable transfer over an unreliable channel.

Three protocols, and the difference between them is how much is in flight and
what happens after a loss.

| protocol | in flight | after a loss |
|---|---|---|
| stop and wait | 1 | resend the one packet |
| go back N | N | resend the packet **and everything after it** |
| selective repeat | N | resend only the lost packet |

Stop and wait is correct and unusable: on a link with a 30 ms round trip and a
packet that takes 8 microseconds to transmit, the sender is busy for less than
a thousandth of the time. Everything else is about filling that gap.
"""

from __future__ import annotations


def utilisation(protocol, window, rtt, transmit):
    """Fraction of the time the sender is transmitting.

    The window multiplies it directly, until it saturates at one. That linear
    relationship is the whole argument for pipelining, and it is why the window
    size is chosen as the bandwidth-delay product rather than by tuning.
    """
    single = transmit / (rtt + transmit)
    return min(1.0, window * single)


def stop_and_wait(packets, loss_pattern=()):
    """Send one packet at a time, waiting for each acknowledgement."""
    lost = set(loss_pattern)
    transmissions = 0
    delivered = 0

    for sequence in range(packets):
        transmissions += 1
        if sequence in lost:
            transmissions += 1
        delivered += 1

    return {"delivered": delivered, "transmissions": transmissions}


def go_back_n(packets, window, loss_pattern=()):
    """Send up to `window` packets, and resend from the loss onwards.

    The receiver discards everything after a gap, so the sender has no choice:
    it retransmits the window. That makes the receiver trivial, one expected
    sequence number and nothing else, and makes a single loss expensive.
    """
    lost = set(loss_pattern)
    transmissions = 0
    base = 0

    while base < packets:
        window_end = min(base + window, packets)
        for sequence in range(base, window_end):
            transmissions += 1

        first_loss = next((sequence for sequence in range(base, window_end)
                           if sequence in lost), None)
        if first_loss is None:
            base = window_end
        else:
            lost.discard(first_loss)
            base = first_loss

    return {"delivered": packets, "transmissions": transmissions}


def selective_repeat(packets, window, loss_pattern=()):
    """Send up to `window` packets and resend only the ones that were lost.

    The receiver buffers out-of-order packets, which costs memory and a second
    window's worth of bookkeeping, and saves every retransmission go-back-N
    would have made. On a link where losses are independent that is the
    difference between usable and not.
    """
    lost = set(loss_pattern)
    transmissions = 0

    for sequence in range(packets):
        transmissions += 1
        if sequence in lost:
            transmissions += 1

    return {"delivered": packets, "transmissions": transmissions}


def window_is_safe(window, sequence_bits, protocol):
    """Whether a window size can be distinguished with the sequence numbers.

    Go-back-N can use `2^k - 1`, because the receiver accepts only the next
    expected number. Selective repeat can use only `2^(k-1)`, because the
    receiver accepts a window of numbers and a retransmission must not look
    like a new packet.

    Getting this wrong produces a protocol that works in testing and duplicates
    data under loss, which is the worst possible failure mode.
    """
    space = 1 << sequence_bits
    if protocol == "selective":
        return window <= space // 2
    return window <= space - 1


def bandwidth_delay_product(rate, rtt):
    """How much data fits in the link, which is the window a sender needs.

    A 1 Gbit/s link with a 30 ms round trip holds nearly 4 MB. A window smaller
    than that leaves the link idle regardless of how fast either end is, which
    is why long fat links need window scaling.
    """
    return rate * rtt / 8
