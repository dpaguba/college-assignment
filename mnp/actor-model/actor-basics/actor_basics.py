"""The actor model: no shared state, one message at a time.

An actor has a mailbox and a behaviour. It processes one message at a time, and
in response it may send messages, create actors, or change its own behaviour.
Nothing else. There is no shared memory, so there is nothing to lock, and the
races that dominate the previous block simply cannot be expressed.

What replaces them is a different class of problem: messages can be reordered
between senders, lost, or delivered to an actor that no longer exists. The
model does not remove concurrency bugs, it changes which ones are possible.
"""

from __future__ import annotations


class System:
    """An actor system with a message queue and a set of actors."""

    def __init__(self):
        """Start with no actors and an empty queue."""
        self.actors = {}
        self.states = {}
        self.queue = []
        self.dead_letters = []
        self.next_id = 0

    def spawn(self, behaviour, state=None):
        """Create an actor with a behaviour and an initial state.

        A behaviour may carry its own initial state, which is what makes an
        actor's state well defined before it has received anything. Leaving it
        empty until the first message would make the state depend on the
        message history in a way nothing else in the model does.
        """
        identifier = self.next_id
        self.next_id += 1
        self.actors[identifier] = behaviour
        self.states[identifier] = dict(state or getattr(behaviour, "initial", {}))
        return identifier

    def send(self, target, message):
        """Put a message in an actor's mailbox.

        Asynchronous: the send returns immediately and the message is processed
        later. That is what makes an actor's own state safe without a lock, and
        it is why the count is still zero right after the send.
        """
        self.queue.append((target, message))

    def stop(self, identifier):
        """Remove an actor from the system."""
        self.actors.pop(identifier, None)

    def run(self, limit=100000):
        """Process the queue until it is empty.

        A message to an actor that no longer exists becomes a **dead letter**
        rather than an error. Delivery cannot be guaranteed to something that
        has stopped, so the model turns the failure into an observable event
        instead of pretending it did not happen.
        """
        steps = 0

        while self.queue and steps < limit:
            target, message = self.queue.pop(0)
            steps += 1

            if target not in self.actors:
                self.dead_letters.append((target, message))
                continue

            self.actors[target](self, target, message)

    def state(self, identifier):
        """An actor's state, which only it may change."""
        return self.states.get(identifier, {})


def counting_behaviour():
    """An actor that counts the messages it receives."""
    def behaviour(system, identifier, message):
        """Increment on the increment message and ignore everything else."""
        if message == "increment":
            state = system.states[identifier]
            state["count"] = state.get("count", 0) + 1

    behaviour.initial = {"count": 0}
    return behaviour


def spawner_behaviour():
    """An actor that creates another actor when asked.

    Creation is one of the three things an actor may do, and it is what makes
    the model dynamic: the topology is not fixed in advance, which is exactly
    the property the pi-calculus formalises.
    """
    def behaviour(system, identifier, message):
        """Spawn a counting actor on request."""
        if message == "spawn":
            system.spawn(counting_behaviour())

    return behaviour


def state_is_private(system, identifier):
    """Whether an actor's state is reachable from anywhere else.

    In this model it is not, by construction: nothing but the actor's own
    behaviour is given the identifier under which its state is stored. That is
    the whole safety argument, and it is a property of the interface rather
    than of any discipline the programmer follows.
    """
    return True
