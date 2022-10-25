"""Buses: who gets to send, and what that decides about the latency.

A priority bus gives the medium to the message with the smallest identifier,
which is how CAN arbitration works and why an important message is never
delayed by an unimportant one. The price is that a low priority message has
no bound at all: a busy bus can starve it indefinitely.

A time slotted bus gives every node a fixed slot, so every message waits at
most one round. The price is the unused bandwidth of a silent node, and the
choice between the two is the choice between a good average and a bound.
"""


def arbitrate(protocol, messages, slot=None):
    """Which message the bus carries next."""
    if protocol == "CAN":
        return min(messages, key=lambda item: item[1])[0]
    if protocol == "TDMA":
        if slot is None:
            raise ValueError("a slotted bus needs the current slot")
        for name, position in messages:
            if position == slot:
                return name
        return None
    raise ValueError("unknown protocol: %s" % protocol)


def worst_case_latency(protocol, nodes, slot):
    """The longest a message can wait, or nothing when there is no bound."""
    if protocol == "TDMA":
        return nodes * slot
    if protocol == "CAN":
        return None
    raise ValueError("unknown protocol: %s" % protocol)


def share(protocol, nodes):
    """The share of the bandwidth a node is guaranteed."""
    if protocol == "TDMA":
        return 1.0 / nodes
    return 0.0


def priority_inversion_on_a_bus():
    """Why a non-preemptable message blocks a higher priority one.

    A frame in flight cannot be interrupted, so the highest priority message
    still waits for the longest frame currently being sent. That blocking is
    bounded and it has to enter the analysis, which is the same pattern as
    resource blocking in the scheduling block.
    """
    return {"blocking": "one frame", "bounded": True}
