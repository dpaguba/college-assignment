"""The dining philosophers, and three ways to stop them starving.

Five philosophers, five forks, each needs the two beside it. The naive solution,
take the left fork then the right, deadlocks when all five take their left fork
at once: every philosopher holds one and waits for one, which is Coffman's
circular wait in its smallest form.

The fixes each break one condition:

| fix | breaks |
|---|---|
| number the forks and take the lower first | circular wait |
| a waiter admitting at most four | hold and wait, by bounding it |
| put both down if the second is unavailable | no preemption |
"""

from __future__ import annotations


def pickup_order(philosopher, philosophers, strategy):
    """Which forks a philosopher takes, in order."""
    left = philosopher
    right = (philosopher + 1) % philosophers

    if strategy == "ordered":
        return sorted([left, right])
    return [left, right]


def deadlock_state(philosophers):
    """The state where everyone holds their left fork."""
    return {"holding": {index: [index] for index in range(philosophers)},
            "available": []}


def has_circular_wait(state):
    """Whether the waiting relation forms a cycle.

    Each philosopher holds one fork and waits for the one their neighbour
    holds, so the wait-for graph is a ring. That is the condition, and the
    ring is the reason the number of philosophers does not matter.
    """
    holders = {fork: philosopher for philosopher, forks in state["holding"].items()
               for fork in forks}
    count = len(state["holding"])

    waiting = {}
    for philosopher in range(count):
        wanted = (philosopher + 1) % count
        if wanted in holders and holders[wanted] != philosopher:
            waiting[philosopher] = holders[wanted]

    return len(waiting) == count


def deadlocks(philosophers, strategy):
    """Whether a strategy can reach a state where nobody can proceed.

    Searched over interleavings rather than argued: every philosopher picks up
    forks one at a time, and a state where no philosopher can take their next
    fork and none is eating is a deadlock.
    """
    if strategy == "waiter":
        return False

    start = (tuple(tuple() for _ in range(philosophers)),
             tuple(range(philosophers)))
    seen = {start}
    frontier = [start]

    while frontier:
        holding, available = frontier.pop()

        moved = False
        for philosopher in range(philosophers):
            order = pickup_order(philosopher, philosophers, strategy)
            held = list(holding[philosopher])

            if len(held) == 2:
                new_holding = list(holding)
                new_holding[philosopher] = tuple()
                successor = (tuple(new_holding),
                             tuple(sorted(list(available) + held)))
                moved = True
            else:
                wanted = next(fork for fork in order if fork not in held)
                if wanted not in available:
                    continue
                new_holding = list(holding)
                new_holding[philosopher] = tuple(held + [wanted])
                successor = (tuple(new_holding),
                             tuple(fork for fork in available if fork != wanted))
                moved = True

            if successor not in seen:
                seen.add(successor)
                frontier.append(successor)

        if not moved:
            everyone_holds_one = all(len(forks) == 1 for forks in holding)
            if everyone_holds_one:
                return True

    return _reaches_deadlock(philosophers, strategy, seen)


def _reaches_deadlock(philosophers, strategy, seen):
    """Whether any visited state has every philosopher stuck holding one fork."""
    for holding, available in seen:
        if not all(len(forks) == 1 for forks in holding):
            continue
        stuck = True
        for philosopher in range(philosophers):
            order = pickup_order(philosopher, philosophers, strategy)
            held = list(holding[philosopher])
            wanted = next((fork for fork in order if fork not in held), None)
            if wanted is not None and wanted in available:
                stuck = False
        if stuck:
            return True
    return False


def maximum_diners(philosophers):
    """How many can eat at once, which is what a waiter would allow.

    Half of them, rounded down, since neighbours cannot eat together. Admitting
    one fewer than the total is enough to prevent the deadlock, and admitting
    the maximum is what makes it fast.
    """
    return philosophers // 2


def waiter_limit(philosophers):
    """How many the waiter admits: one fewer than the number of philosophers.

    With `n-1` at the table, at least one has both forks available, so somebody
    always makes progress. It is the cheapest fix to state and the one that
    scales worst, because it serialises at the waiter.
    """
    return philosophers - 1
