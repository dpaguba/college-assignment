# The model

An actor has private state, an address, and a mailbox, and it handles one
message at a time. From that last clause everything else follows: there is no
concurrency inside an actor, so there are no locks, and a message is handled
completely or not at all.

`become` sets the behaviour for the **next** message rather than changing
state now. The difference is that no half-changed state is ever observable,
which is what atomicity means here, without a lock anywhere.

## What is guaranteed, and by whom

| | Agha 1985 | typical implementation |
|---|---|---|
| eventual delivery | yes | no, a message can be lost |
| order between two actors | no | yes |

Both are weaker than they look. The theory allows a message to be arbitrarily
late; the implementation guarantees order only per pair, which says nothing
once three actors are involved.

## Against shared memory

Shared memory has the problem of simultaneous access and the tool of locks.
Actors have the problem of the protocol and the tool of a state machine per
actor. The difficulty does not disappear, it moves: the failure mode changes
from a lost update to a message the actor was not expecting in this state.
