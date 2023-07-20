# Message ordering and delivery

Two questions that get confused with each other: in what order messages
arrive, and how many times they arrive.

## Ordering

The guarantee is per sender-receiver pair. If A sends m1 then m2 to B, B sees
m1 before m2. Nothing is promised about messages from different senders, so
with two senders and two messages each, four orders are possible and the
system must be correct under all of them.

Causality is the weaker property that matters in practice: if B's message to C
was sent in response to A's message to B, then C must not see the effect
before the cause. Per-pair ordering does not give this on its own, which is
what vector clocks and similar mechanisms exist to restore.

## Delivery

| Semantics | Deliveries after 2 failures | Requires |
|---|---|---|
| at most once | 0 | nothing |
| at least once | 3 | retries |
| exactly once | 1 | retries and deduplication at the receiver |

Exactly-once asks nothing extra of the network. It is at-least-once plus
bookkeeping at the receiver, and the bookkeeping is unbounded in general,
which is why systems that advertise it usually mean at-least-once with
idempotent handlers. Making the handler idempotent gets the same outcome for
free, and that is why so much distributed design is about idempotence rather
than about delivery.
