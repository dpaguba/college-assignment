"""What an actor system guarantees about message order, and what it does not.

The guarantee is **per sender-receiver pair**: messages from A to B arrive in
the order A sent them. Nothing is promised about messages from different
senders, so a receiver seeing a message from A and one from B cannot conclude
anything about which was sent first.

That is much weaker than it sounds and much stronger than nothing. It is enough
to reason about a protocol between two actors, and not enough to reason about
three without adding sequence numbers or a causal order.
"""

from __future__ import annotations

import itertools


def delivered(messages):
    """The order messages arrive when they share a sender and a receiver."""
    return [payload for _, _, payload in messages]


def possible_orders(messages):
    """Every delivery order the guarantee permits.

    All interleavings that preserve the order within each sender-receiver pair.
    Two messages from different senders give two orders; adding a second
    message from one of them gives three rather than six, because two of the
    six violate the pairwise order.
    """
    by_pair = {}
    for sender, receiver, payload in messages:
        by_pair.setdefault((sender, receiver), []).append(payload)

    orders = set()
    for permutation in itertools.permutations(payload for _, _, payload in messages):
        valid = True
        for sequence in by_pair.values():
            positions = [permutation.index(payload) for payload in sequence]
            if positions != sorted(positions):
                valid = False
                break
        if valid:
            orders.add(permutation)

    return sorted(orders)


def respects_causality(messages, observed):
    """Whether an observed order is consistent with the causal chain.

    A message sent **in response to** another cannot be observed first. The
    per-pair guarantee does not give this, because the two messages have
    different senders, which is why systems that need it carry vector clocks.
    """
    causes = {}
    for index, (sender, receiver, payload) in enumerate(messages):
        for earlier_index, (_, earlier_receiver, earlier_payload) in enumerate(messages):
            if earlier_index < index and earlier_receiver == sender:
                causes.setdefault(payload, set()).add(earlier_payload)

    for payload, required in causes.items():
        for earlier in required:
            if observed.index(earlier) > observed.index(payload):
                return False

    return True


def delivery_count(semantics, failures):
    """How many times a message is delivered under each guarantee.

    | semantics | on failure | needs |
    |---|---|---|
    | at most once | 0 | nothing |
    | at least once | 2 or more | retries |
    | exactly once | 1 | retries **and** deduplication |

    The third asks nothing extra of the network. It is the second plus
    bookkeeping at the receiver, which is why it costs state and why systems
    that claim it usually mean the second with idempotent handlers.
    """
    if semantics == "at most once":
        return 0 if failures else 1
    if semantics == "at least once":
        return 1 + failures
    return 1


def is_idempotent_safe(semantics, handler_idempotent):
    """Whether a handler can live with a delivery guarantee.

    An idempotent handler makes at-least-once behave like exactly-once without
    any deduplication state. That is why so much distributed design is about
    making operations idempotent rather than about making delivery exact.
    """
    if semantics == "exactly once":
        return True
    return handler_idempotent
