# The actor model

| Topic | |
|---|---|
| [actor-basics](actor-basics/) | mailbox, private state, one message at a time |
| [message-ordering](message-ordering/) | per-pair ordering, causality, delivery counts |
| [supervision](supervision/) | trees, restart, stop, escalate |

Shared memory with locks makes correctness a property of every access.
Message passing makes it a property of one actor's behaviour, and the previous
block's problems mostly stop existing: no shared variable, no race on it.

What remains is ordering and failure. Ordering is guaranteed only per
sender-receiver pair, so any protocol that assumes more is wrong under
interleaving the tests will not show. Failure is handled by the tree rather
than at the point it occurs, which keeps recovery where the context is.

The Akka project from the practical is in [assignment](../assignment/).
