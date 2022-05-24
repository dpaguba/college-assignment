# The actor model in π

| Actor | π |
|---|---|
| create | `(νa)P`, a restriction |
| send | `ā⟨v⟩.P`, an output |
| become | the choice of body behind the input |
| address | a name |
| mailbox | a replicated input on that name |

An actor is `!a(msg).behaviour`. The replication is what keeps it ready: after
each message it provides another copy.

That is the claim of lecture 10, and it means the actor model needs no theory
of its own; it is a fragment of the calculus.

## What the encoding does not carry over

A replicated input accepts any number of messages at once, each copy handling
one, all in parallel. An actor handles one message at a time. To get that
back, the body has to take a token from a channel at the start and put it
back at the end, which is a lock, and the fact that a lock becomes necessary
is a precise measure of where the encoding and the model part company.

The mailbox order goes too: in the calculus the messages lie side by side
with no order, which matches Agha's theory and not the usual
implementations.
