"""What the thread model cannot express, and why the lecture starts there.

Threads with shared memory are the default model and the lecture spends a
session on its limits. Two of them matter for embedded systems: the result of
a program is not determined by the program, because the interleaving decides
it, and there is no way to say when something has to happen, because time is
not part of the model at all.

A dataflow model has neither problem, and that is the argument for the models
in the rest of this block.
"""


def interleavings():
    """The possible results of two threads incrementing a shared counter.

    Each thread reads, adds and writes. Interleaving the reads loses one
    update, so the counter ends at 1 or at 2 depending on the order, and
    nothing in the program says which.
    """
    outcomes = set()
    for order in ("aabb", "abab", "abba", "baab", "baba", "bbaa"):
        value = 0
        held = {"a": None, "b": None}
        for step in order:
            if held[step] is None:
                held[step] = value
            else:
                value = held[step] + 1
        outcomes.add(value)
    return outcomes


def dataflow_outcomes():
    """The possible results of the same computation as a dataflow graph.

    An actor fires when its inputs are present and writes to its own output,
    so there is no shared cell to race over and exactly one result.
    """
    return {2}


def von_neumann_limits():
    """The limits of the thread model that the lecture lists."""
    return ["nondeterminism", "no notion of time", "no bound on interference",
            "composition is not modular"]


def can_express(requirement):
    """Whether the thread model can state a requirement."""
    expressible = {"mutual exclusion": True, "ordering": True,
                   "deadline": False, "period": False, "jitter": False}
    if requirement not in expressible:
        raise ValueError("unknown requirement: %s" % requirement)
    return expressible[requirement]
