# Actor basics

An actor has a mailbox, private state, and a behaviour that runs one message
at a time. Those three together remove the race conditions the previous block
spent its time hunting: state that only one thread touches needs no lock.

## What the model actually guarantees

One message at a time per actor, and nothing more. Two actors run genuinely in
parallel, so the ordering *between* them is unconstrained, and an actor's
state is safe only because no one else can reach it. Handing out a mutable
object through a message breaks the guarantee immediately, which is why actor
libraries insist that messages be immutable.

An actor can create other actors, send messages, and change its own behaviour
for the next message. The third is what replaces a state machine written by
hand: instead of a field holding a mode and a switch reading it, the behaviour
itself becomes the state.

## Behaviour and initial state

A behaviour declares the state it starts with, so spawning an actor from a
behaviour gives a fresh, complete state rather than one filled in by the first
message that happens to arrive. A counter that starts undefined and becomes
zero on first use works until two messages race, which is the ordinary shape
of this bug.

## What it does not solve

Deadlock survives the move to actors. Two actors that each wait for a reply
from the other are as stuck as two threads holding each other's mutex, and the
symptom is quieter: no lock is held, no thread is blocked in the operating
system, and both mailboxes simply stop draining. The Akka assignment in
[assignment](../../assignment/) shows the shape of the problem, where actors
address each other through references handed over at construction.
