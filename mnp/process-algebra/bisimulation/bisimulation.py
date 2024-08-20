"""Strong and weak bisimulation, trace equivalence, and a witness.

Trace equivalence asks which sequences of actions are possible. Bisimulation
asks something stronger: at every point the two processes must offer the same
choices, so a process that commits early is distinguished from one that keeps
its options open. The classic pair ``a.(b + c)`` and ``a.b + a.c`` has the
same traces and fails bisimulation, and this module produces the trace after
which they differ.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ccs"))
import ccs


def _successors(process, action, environment):
    """The states reachable by one transition with the given label."""
    return [following for label, following in ccs.transitions(process, environment)
            if label == action]


def strongly_bisimilar(first, second, environment=None, depth=12):
    """Check strong bisimulation coinductively, bounded by depth."""
    environment = environment or {}
    return _bisimilar(first, second, environment, depth, weak=False, seen=set())


def weakly_bisimilar(first, second, environment=None, depth=12):
    """Weak bisimulation, where ``tau`` steps are unobservable."""
    environment = environment or {}
    return _bisimilar(first, second, environment, depth, weak=True, seen=set())


def _tau_closure(process, environment):
    """Every state reachable by internal steps alone, including this one."""
    frontier, closure = [process], []
    while frontier:
        current = frontier.pop()
        if any(current == item for item in closure):
            continue
        closure.append(current)
        frontier.extend(_successors(current, ccs.TAU, environment))
    return closure


def _weak_successors(process, action, environment):
    """Successors of the observable step, with internal steps absorbed."""
    result = []
    for before in _tau_closure(process, environment):
        for middle in _successors(before, action, environment):
            result.extend(_tau_closure(middle, environment))
    return result


def _bisimilar(first, second, environment, depth, weak, seen):
    """The mutual simulation check, memoised on the pairs already assumed."""
    key = (repr(first), repr(second), weak)
    if key in seen:
        return True
    if depth == 0:
        return True
    seen = seen | {key}
    labels = set(ccs.actions(first, environment)) | set(ccs.actions(second, environment))
    if weak:
        labels.discard(ccs.TAU)
        if not _tau_matched(first, second, environment, depth, seen):
            return False
    for action in labels:
        if weak:
            left = _weak_successors(first, action, environment)
            right = _weak_successors(second, action, environment)
        else:
            left = _successors(first, action, environment)
            right = _successors(second, action, environment)
        if bool(left) != bool(right):
            return False
        for candidate in left:
            if not any(_bisimilar(candidate, other, environment, depth - 1, weak, seen)
                       for other in right):
                return False
        for candidate in right:
            if not any(_bisimilar(candidate, other, environment, depth - 1, weak, seen)
                       for other in left):
                return False
    return True


def _tau_matched(first, second, environment, depth, seen):
    """Whether each internal step is answered by internal steps on the other side.

    A weak bisimulation may answer a ``tau`` with no move at all, so the
    matching states are drawn from the other side's tau-closure. Omitting this
    clause makes ``tau.a + tau.b`` look equivalent to ``a + b``, which is the
    difference between choosing internally and offering a choice.
    """
    for left, right in ((first, second), (second, first)):
        for after in _successors(left, ccs.TAU, environment):
            if not any(_bisimilar(after, candidate, environment, depth - 1,
                                  True, seen)
                       for candidate in _tau_closure(right, environment)):
                return False
    return True


def observable_traces(process, depth, environment=None):
    """Traces with internal steps removed, which is what an observer records."""
    visible = set()
    for trace in traces(process, depth, environment):
        visible.add(tuple(action for action in trace if action != ccs.TAU))
    return sorted(visible)


def traces(process, depth, environment=None):
    """Every trace up to the given length, sorted."""
    environment = environment or {}
    result = {()}
    frontier = [((), process)]
    for _ in range(depth):
        following = []
        for trace, current in frontier:
            for action, target in ccs.transitions(current, environment):
                extended = trace + (action,)
                result.add(extended)
                following.append((extended, target))
        frontier = following
    return sorted(result)


def trace_equivalent(first, second, depth, environment=None):
    """Compare trace sets, the weaker of the two criteria."""
    return traces(first, depth, environment) == traces(second, depth, environment)


def distinguishing_trace(first, second, environment=None, depth=6):
    """Find a trace after which the available actions differ.

    The witness is what turns a failed bisimulation into an argument: after
    ``a`` one process still offers both ``b`` and ``c`` while the other has
    already committed to one of them.
    """
    environment = environment or {}
    frontier = [((), first, second)]
    for _ in range(depth):
        following = []
        for trace, left, right in frontier:
            left_actions = set(ccs.actions(left, environment))
            right_actions = set(ccs.actions(right, environment))
            if left_actions != right_actions:
                return {"trace": list(trace),
                        "only_left": sorted(left_actions - right_actions),
                        "only_right": sorted(right_actions - left_actions)}
            for action in left_actions:
                for after_left in _successors(left, action, environment):
                    for after_right in _successors(right, action, environment):
                        following.append((trace + (action,), after_left, after_right))
        frontier = following
    return None
