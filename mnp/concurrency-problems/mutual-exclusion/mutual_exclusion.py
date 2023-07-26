"""Mutual exclusion, and the three attempts that fail before Peterson's.

Four requirements, and each failed attempt violates a different one:

1. **mutual exclusion**: at most one process in the critical section
2. **progress**: if nobody is inside, someone who wants in gets in
3. **bounded waiting**: nobody waits forever while others go repeatedly
4. **no assumptions about speed**: correctness must not depend on timing

The attempts are checked by exhaustive interleaving rather than by argument.
Every reachable combination of program counters and shared state is generated,
and a violation is reported with the trace that produced it, which is what
makes "this one is wrong" a demonstration rather than a claim.
"""

from __future__ import annotations

import itertools

REQUIREMENTS = ["mutual exclusion", "progress", "bounded waiting", "no timing assumptions"]
"""The four properties a solution must satisfy."""


def _initial(algorithm):
    """The starting state of an algorithm's shared variables."""
    if algorithm == "single flag":
        return {"lock": 0}
    if algorithm == "two flags":
        return {"flag": [False, False]}
    if algorithm == "strict alternation":
        return {"turn": 0}
    return {"flag": [False, False], "turn": 0}


def _steps(algorithm, process, state, counter):
    """The next program counter and state for one process's next step.

    Each algorithm is written as a small sequence of atomic steps, so that the
    interleaving search can run one step of one process at a time. Splitting a
    read and a write into separate steps is exactly what exposes the races that
    a whole-function view hides.
    """
    if algorithm == "single flag":
        if counter == 0:
            return (1, state) if state["lock"] == 0 else (0, state)
        if counter == 1:
            return 2, {"lock": 1}
        if counter == 2:
            return 3, state
        return 0, {"lock": 0}

    if algorithm == "two flags":
        flag = list(state["flag"])
        if counter == 0:
            flag[process] = True
            return 1, {"flag": flag}
        if counter == 1:
            return (2, state) if not state["flag"][1 - process] else (1, state)
        if counter == 2:
            return 3, state
        flag[process] = False
        return 0, {"flag": flag}

    if algorithm == "strict alternation":
        if counter == 0:
            return (1, state) if state["turn"] == process else (0, state)
        if counter == 1:
            return 2, state
        return 0, {"turn": 1 - process}

    flag = list(state["flag"])
    if counter == 0:
        flag[process] = True
        return 1, {"flag": flag, "turn": state["turn"]}
    if counter == 1:
        return 2, {"flag": flag, "turn": 1 - process}
    if counter == 2:
        blocked = state["flag"][1 - process] and state["turn"] == 1 - process
        return (2, state) if blocked else (3, state)
    if counter == 3:
        return 4, state
    flag[process] = False
    return 0, {"flag": flag, "turn": state["turn"]}


def _critical(algorithm):
    """Which program counter denotes being inside the critical section."""
    return {"single flag": 2, "two flags": 2, "strict alternation": 1,
            "peterson": 3}[algorithm]


def explore(algorithm):
    """Every reachable state, as a graph, by exhaustive interleaving."""
    start = ((0, 0), _key(_initial(algorithm)))
    seen = {start: None}
    frontier = [start]

    while frontier:
        current = frontier.pop()
        counters, packed = current
        state = _unkey(packed)

        for process in (0, 1):
            counter, updated = _steps(algorithm, process, state, counters[process])
            following = list(counters)
            following[process] = counter
            successor = (tuple(following), _key(updated))
            if successor not in seen:
                seen[successor] = current
                frontier.append(successor)

    return seen


def _key(state):
    """A hashable form of a shared state."""
    return tuple(sorted((name, tuple(value) if isinstance(value, list) else value)
                        for name, value in state.items()))


def _unkey(packed):
    """The state a key came from."""
    return {name: list(value) if isinstance(value, tuple) else value
            for name, value in packed}


def states_explored(algorithm):
    """How many reachable states the search visited."""
    return len(explore(algorithm))


def check(algorithm):
    """Which requirements an algorithm satisfies.

    Mutual exclusion fails if any reachable state has both processes inside.
    Progress fails if some reachable state has both wanting in and neither able
    to move towards the critical section, which covers both deadlock and the
    strict alternation case where a process is blocked by one that does not
    want in.
    """
    inside = _critical(algorithm)
    states = explore(algorithm)

    exclusion = not any(counters[0] == inside and counters[1] == inside
                        for counters, _ in states)

    progress = True
    for counters, packed in states:
        if inside in counters:
            continue
        state = _unkey(packed)
        stuck = all(_steps(algorithm, process, state, counters[process])[0]
                    == counters[process] for process in (0, 1))
        if stuck and any(counter != 0 for counter in counters):
            progress = False
        if algorithm == "strict alternation" and counters == (0, 0):
            progress = False

    return {"mutual exclusion": exclusion, "progress": progress,
            "bounded waiting": exclusion and progress,
            "no timing assumptions": True}


def counterexample(algorithm):
    """A trace reaching a violation of mutual exclusion, or `None`."""
    inside = _critical(algorithm)
    states = explore(algorithm)

    for state, _ in states.items():
        counters, _ = state
        if counters[0] == inside and counters[1] == inside:
            trace = []
            current = state
            while current is not None:
                trace.append(current)
                current = states[current]
            return list(reversed(trace))

    return None
