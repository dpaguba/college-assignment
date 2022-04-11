"""Deadlocks: the four conditions, detection, and the banker's algorithm.

A deadlock needs all four of Coffman's conditions at once, and breaking any one
of them prevents it. Three are usually impractical to break, which is why the
fourth, circular wait, is the one real systems attack: acquire locks in a fixed
global order and no cycle can form.

Detection is a cycle search in the wait-for graph. Avoidance is the banker's
algorithm, which refuses any request that would leave the system unable to
finish, and needs every process to declare its maximum demand in advance.
"""

from __future__ import annotations

COFFMAN = [
    "mutual exclusion",
    "hold and wait",
    "no preemption",
    "circular wait",
]
"""The four conditions, all of which a deadlock needs."""


def has_deadlock(wait_for):
    """Whether the wait-for graph contains a cycle."""
    return find_cycle(wait_for) is not None


def find_cycle(wait_for):
    """A cycle in the wait-for graph, or `None`.

    The cycle is the useful output rather than the boolean: a detector that
    reports a deadlock without saying who is in it leaves the operator with
    nothing to kill.
    """
    colour = {}
    stack = []

    def visit(node):
        """Depth-first search, returning a cycle when it revisits the stack."""
        colour[node] = "grey"
        stack.append(node)

        for target in wait_for.get(node, []):
            if colour.get(target) == "grey":
                return stack[stack.index(target):]
            if colour.get(target) is None:
                found = visit(target)
                if found:
                    return found

        stack.pop()
        colour[node] = "black"
        return None

    for node in wait_for:
        if colour.get(node) is None:
            found = visit(node)
            if found:
                return found

    return None


def ordered_acquisition_is_safe(orders):
    """Whether every process acquires the locks in one global order.

    The practical prevention. Two threads taking the same two locks in opposite
    orders can deadlock; the same two threads taking them in the same order
    cannot, whatever the timing. That is why a codebase with many locks
    publishes an order and treats violating it as a bug even when nothing
    hangs.
    """
    positions = {}
    for order in orders:
        for index, name in enumerate(order):
            positions.setdefault(name, []).append(index)

    reference = orders[0]
    ranking = {name: index for index, name in enumerate(reference)}

    for order in orders[1:]:
        relevant = [name for name in order if name in ranking]
        ranks = [ranking[name] for name in relevant]
        if ranks != sorted(ranks):
            return False

    return True


class State:
    """A snapshot for the banker's algorithm."""

    def __init__(self, available, maximum, allocation):
        """Record what is free, what each process may need and what it holds."""
        self.available = list(available)
        self.maximum = [list(row) for row in maximum]
        self.allocation = [list(row) for row in allocation]

    def need(self):
        """What each process may still request."""
        return [[maximum - allocated for maximum, allocated in zip(row, held)]
                for row, held in zip(self.maximum, self.allocation)]


def safe_sequence(state):
    """An order in which every process can finish, or `None`.

    The definition of a safe state: some order exists in which each process can
    get its remaining need from what is free plus what the earlier ones
    release. A safe state is not deadlock-free by luck, it is deadlock-free by
    construction.
    """
    work = list(state.available)
    need = state.need()
    finished = [False] * len(need)
    sequence = []

    for _ in range(len(need)):
        for index, row in enumerate(need):
            if finished[index]:
                continue
            if all(requirement <= have for requirement, have in zip(row, work)):
                work = [have + held for have, held in zip(work, state.allocation[index])]
                finished[index] = True
                sequence.append(index)
                break
        else:
            return None

    return sequence


def is_safe(state):
    """Whether a safe sequence exists."""
    return safe_sequence(state) is not None


def request_granted(state, process, request):
    """Whether the banker grants a request.

    Granted only if the request is within the declared need and within what is
    available, **and** the resulting state is still safe. The third test is the
    algorithm: the first two are bookkeeping, and a system that checks only
    them is doing nothing about deadlock at all.
    """
    need = state.need()

    if any(amount > allowed for amount, allowed in zip(request, need[process])):
        return False
    if any(amount > have for amount, have in zip(request, state.available)):
        return False

    trial = State(
        available=[have - amount for have, amount in zip(state.available, request)],
        maximum=state.maximum,
        allocation=[list(row) for row in state.allocation])
    trial.allocation[process] = [held + amount for held, amount
                                 in zip(trial.allocation[process], request)]

    return is_safe(trial)


def why_avoidance_is_rare():
    """Why the banker's algorithm is taught and not used.

    It needs every process to declare its maximum demand before it starts,
    which almost none can, and it runs a safety check on every request, which
    costs time proportional to processes times resources. Real systems detect
    and recover, or prevent by lock ordering, or ignore the problem and reboot,
    which is what the term "ostrich algorithm" is about.
    """
    return ["maximum demand must be declared in advance",
            "a safety check on every request is expensive",
            "the number of processes and resources changes constantly"]
