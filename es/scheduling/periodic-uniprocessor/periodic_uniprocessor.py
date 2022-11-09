"""Utilisation tests for periodic tasks on one processor.

Two results, and the difference between them is the point. The rate monotonic
bound is sufficient and not necessary: a set above it may still be
schedulable, and the exam's second task set is exactly such a case. The
earliest deadline first test is both sufficient and necessary, so a set is
schedulable exactly when its utilisation fits on the processor.

The bound falls from 1 for a single task to the natural logarithm of two for
many, which is the number usually quoted and the reason a rate monotonic
system is often designed for about 69 percent load.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "rtos",
                                "task-model"))
import task_model


def rm_bound(count):
    """The Liu and Layland bound for the given number of tasks."""
    return count * (2 ** (1 / count) - 1)


def rm_utilisation_test(tasks):
    """Whether the set passes the sufficient test for rate monotonic order."""
    return float(task_model.utilisation(tasks)) <= rm_bound(len(tasks))


def edf_test(tasks):
    """Whether the set is schedulable under earliest deadline first.

    Exact for implicit deadlines: the condition is that the utilisation does
    not exceed one, and nothing else matters, which is why this policy is
    called optimal for the uniprocessor case.
    """
    if any(task.deadline < task.period for task in tasks):
        return sum(task.density for task in tasks) <= 1
    return task_model.utilisation(tasks) <= 1


def hyperbolic_bound_test(tasks):
    """The tighter sufficient test, which accepts more sets than the bound."""
    product = 1.0
    for task in tasks:
        product *= float(task.utilisation) + 1
    return product <= 2.0
