"""TCP connection management: the handshake, the close, and the states.

Setting up takes three messages and tearing down takes four, and the asymmetry
is not an accident. A connection is two independent byte streams, so each
direction is closed separately, and the side that closes first has to wait
afterwards in case its last acknowledgement was lost.

That wait is `TIME_WAIT`, and it lasts twice the maximum segment lifetime. It is
why a server that has just been restarted cannot immediately rebind its port,
and why the option to override that exists and is dangerous.
"""

from __future__ import annotations

STATES = ["CLOSED", "LISTEN", "SYN SENT", "SYN RECEIVED", "ESTABLISHED",
          "FIN WAIT 1", "FIN WAIT 2", "CLOSE WAIT", "LAST ACK", "TIME WAIT"]
"""The states of the connection diagram the lecture draws."""


def handshake():
    """The three messages that open a connection.

    Three rather than two, because both sides must choose an initial sequence
    number and learn the other's. Two messages would leave one side's number
    unacknowledged, and a delayed duplicate of an old connection request could
    then be accepted as a new connection.
    """
    return [
        {"from": "client", "flags": "SYN", "sets": "client sequence number"},
        {"from": "server", "flags": "SYN ACK", "sets": "server sequence number"},
        {"from": "client", "flags": "ACK", "sets": "acknowledges the server's"},
    ]


def close():
    """The four messages that close a connection."""
    return [
        {"from": "initiator", "flags": "FIN"},
        {"from": "responder", "flags": "ACK"},
        {"from": "responder", "flags": "FIN"},
        {"from": "initiator", "flags": "ACK"},
    ]


def next_state(state, event):
    """The state a connection moves to on an event."""
    table = {
        ("CLOSED", "passive open"): "LISTEN",
        ("CLOSED", "active open"): "SYN SENT",
        ("LISTEN", "SYN"): "SYN RECEIVED",
        ("SYN SENT", "SYN ACK"): "ESTABLISHED",
        ("SYN RECEIVED", "ACK"): "ESTABLISHED",
        ("ESTABLISHED", "FIN"): "CLOSE WAIT",
        ("ESTABLISHED", "close"): "FIN WAIT 1",
        ("FIN WAIT 1", "ACK"): "FIN WAIT 2",
        ("FIN WAIT 2", "FIN"): "TIME WAIT",
        ("CLOSE WAIT", "close"): "LAST ACK",
        ("LAST ACK", "ACK"): "CLOSED",
        ("TIME WAIT", "timeout"): "CLOSED",
    }
    return table.get((state, event), state)


def time_wait_duration(segment_lifetime):
    """How long the closing side waits, in the same units as the lifetime.

    Twice the maximum segment lifetime: once for its final acknowledgement to
    arrive, and once for any retransmitted FIN to have died. Shortening it
    risks accepting a segment from a previous connection with the same port
    pair.
    """
    return 2 * segment_lifetime


def is_loss(duplicate_acks):
    """Whether duplicate acknowledgements indicate a loss.

    Three, not one. A single duplicate is usually reordering, and reacting to
    it would halve the window every time a packet took a different route. Three
    is a threshold chosen by measurement, not by derivation.
    """
    return duplicate_acks >= 3


def next_sequence(sequence, payload, syn=False, fin=False):
    """The next sequence number, counting bytes and the two flags.

    TCP numbers bytes rather than segments, and SYN and FIN each consume one
    number without carrying data. That is what makes them acknowledgeable and
    therefore retransmittable.
    """
    return sequence + payload + (1 if syn else 0) + (1 if fin else 0)


def receive_window(buffer_size, buffered):
    """How much the receiver still accepts, which is flow control.

    Distinct from congestion control: this protects the **receiver** from a
    fast sender, and congestion control protects the **network**. A sender is
    limited by the smaller of the two, and confusing them is the standard
    mistake.
    """
    return max(0, buffer_size - buffered)
