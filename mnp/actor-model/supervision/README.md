# Supervision

Actors are arranged in a tree, and a failure travels up it. The parent decides
what happens, choosing between three strategies.

| Strategy | Effect on the failed actor | Effect on its siblings |
|---|---|---|
| restart | fresh state, same reference | none |
| stop | terminated | none |
| escalate | parent fails too | the parent's decision reaches them |

Restart keeps the actor reference valid, so senders holding it do not need to
learn about the failure. The state is discarded, which is the point: the state
is what became inconsistent.

## Let it crash

Handling every error where it happens spreads recovery logic through code that
has no way to know what recovery means. Letting an actor fail and having its
supervisor decide keeps the decision at the level that has the context, and
the recovery becomes one strategy in one place instead of a check at every
call site.

The limit is that restarting only helps when the state is what went wrong. An
actor that fails because a message is malformed will fail again on the same
message, and a supervisor that restarts it forever produces a loop rather than
a recovery. That is why supervisors carry restart limits and why the escalate
strategy exists.

## Failure does not travel sideways

A sibling is unaffected unless the parent escalates or explicitly stops it.
The tree shape is what bounds the blast radius, so grouping actors under a
supervisor is a design decision about which failures should be shared.
