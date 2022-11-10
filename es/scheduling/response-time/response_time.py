"""Response time analysis: the exact test for fixed priorities.

The response time of a task is its own cost plus the interference from every
higher priority task, and the interference depends on the response time, so
the equation is solved by iteration from the sum of the costs upwards. The
iteration increases and is bounded by the deadline, so it terminates.

The exam's two task sets differ only in the third task and the analysis
separates them: 27 against a deadline of 25 in the first, 18 against 20 in
the second. Both fail the utilisation test, so the exact analysis is what
decides them.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "rtos",
                                "task-model"))
import task_model


def response_times(tasks, policy="RM", blocking=None):
    """The worst case response time of every task."""
    blocking = blocking or {}
    ordered = task_model.priority_order(tasks, policy)
    result = {}
    for index, task in enumerate(ordered):
        higher = ordered[:index]
        result[task.name] = _fixed_point(task, higher,
                                         blocking.get(task.name, 0))
    return result


def _fixed_point(task, higher, blocking):
    """The smallest solution of the response time equation."""
    current = task.cost + blocking
    for _ in range(10000):
        interference = sum(math.ceil(current / other.period) * other.cost
                           for other in higher)
        following = task.cost + blocking + interference
        if following == current:
            return current
        if following > task.deadline * 10:
            return following
        current = following
    raise ValueError("the iteration did not settle")


def iteration(tasks, name, policy="RM"):
    """Every value the iteration takes for one task, for inspection."""
    ordered = task_model.priority_order(tasks, policy)
    index = [task.name for task in ordered].index(name)
    task, higher = ordered[index], ordered[:index]
    steps = [task.cost]
    current = task.cost
    for _ in range(1000):
        interference = sum(math.ceil(current / other.period) * other.cost
                           for other in higher)
        following = task.cost + interference
        if following == current:
            return steps
        steps.append(following)
        current = following
    return steps


def is_schedulable(tasks, policy="RM", blocking=None):
    """Whether every task finishes before its deadline."""
    times = response_times(tasks, policy, blocking)
    return all(times[task.name] <= task.deadline for task in tasks)
