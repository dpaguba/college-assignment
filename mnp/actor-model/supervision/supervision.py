"""Supervision: failure as a message to a parent.

An actor that fails does not crash the system. Its parent decides what happens,
and the choice is one of a few strategies: restart the child, stop it, or
escalate the failure to its own parent.

The point is that error handling becomes **structural** rather than local. The
code that fails does not decide what to do about it, and the code that decides
is not tangled into the code that works. That separation is what "let it crash"
means, and it is the opposite of wrapping every call in a handler.
"""

from __future__ import annotations


class Tree:
    """A supervision hierarchy of actors."""

    def __init__(self):
        """Start with no actors."""
        self.parents = {}
        self.strategies = {}
        self.living = set()
        self.restart_counts = {}
        self.next_id = 0

    def spawn(self, parent, strategy="restart"):
        """Create an actor under a parent, with a strategy for its children."""
        identifier = self.next_id
        self.next_id += 1
        self.parents[identifier] = parent
        self.strategies[identifier] = strategy
        self.living.add(identifier)
        self.restart_counts[identifier] = 0
        return identifier

    def fail(self, identifier):
        """Report a failure and apply the responsible parent's strategy.

        The failure travels **up**, never sideways: a sibling is untouched
        unless the parent's strategy says otherwise. That containment is the
        reason a supervision tree is a tree and not a set of handlers.
        """
        parent = self.parents.get(identifier)

        while parent is not None and self.strategies[parent] == "escalate":
            identifier = parent
            parent = self.parents.get(parent)

        if parent is None:
            self.living.discard(identifier)
            return {"action": "stop", "handled_by": None}

        strategy = self.strategies[parent]

        if strategy == "restart":
            self._restart(identifier)
            return {"action": "restart", "handled_by": parent}

        self._stop(identifier)
        return {"action": "stop", "handled_by": parent}

    def _restart(self, identifier):
        """Restart an actor and everything beneath it.

        Restarting a parent restarts its children, because their state was
        derived from the parent's and may be inconsistent with the new one.
        That is the rule people find surprising, and it is what makes a restart
        a recovery rather than a patch.
        """
        self.living.add(identifier)
        self.restart_counts[identifier] += 1

        for child, parent in self.parents.items():
            if parent == identifier:
                self._restart(child)

    def _stop(self, identifier):
        """Stop an actor and everything beneath it."""
        self.living.discard(identifier)

        for child, parent in self.parents.items():
            if parent == identifier:
                self._stop(child)

    def alive(self, identifier):
        """Whether an actor is running."""
        return identifier in self.living

    def restarts(self, identifier):
        """How many times an actor has been restarted."""
        return self.restart_counts.get(identifier, 0)


def strategies():
    """The strategies a supervisor may apply, and what each is for."""
    return {
        "restart": "the failure is transient, and fresh state will do",
        "stop": "the actor cannot recover and its work is not needed",
        "escalate": "this supervisor does not know how to decide",
    }


def why_let_it_crash():
    """Why a supervised system handles fewer errors and survives more.

    Handling an error where it happens means writing recovery code for a state
    that is by definition unexpected. Restarting from a known state is simpler
    and covers failures nobody predicted, which is most of them. The cost is
    that state has to be recoverable, which is a design constraint rather than
    a free property.
    """
    return ["recovery code runs from a known state, not an unexpected one",
            "one strategy covers failures nobody enumerated",
            "the price is that actor state must be reconstructible"]
