"""Several processors, and why the single processor results do not carry over.

Partitioning assigns each task to a processor once, which turns scheduling
into bin packing and inherits its waste: three tasks of utilisation 0.6 do
not fit on two processors even though the total is 1.8.

Global scheduling migrates tasks and defeats the utilisation argument in a
different way. Dhall's effect is the standard example: a set with utilisation
just above one misses deadlines on two processors, because the heavy task
cannot use more than one processor at a time.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "rtos",
                                "task-model"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "periodic-uniprocessor"))
import periodic_uniprocessor as periodic
import task_model


def partition(tasks, processors, rule="first fit"):
    """Assigns the tasks to processors, or reports that they do not fit."""
    order = sorted(tasks, key=lambda task: -task.utilisation) \
        if rule == "decreasing" else list(tasks)
    bins = [[] for _ in range(processors)]
    for task in order:
        for index, bin_content in enumerate(bins):
            candidate = bin_content + [task]
            if periodic.edf_test(candidate):
                bins[index] = candidate
                break
        else:
            return {"assignment": None, "rule": rule, "tasks": tasks}
    return {"assignment": bins, "rule": rule, "tasks": tasks}


def wasted(report):
    """The capacity the packing leaves unused, as a share of one processor."""
    if report["assignment"] is None:
        return None
    processors = len(report["assignment"])
    used = sum(task_model.utilisation(bin_content)
               for bin_content in report["assignment"])
    return float(processors - used) / processors


def global_edf_bound(processors):
    """The utilisation bound for global earliest deadline first.

    Far below the processor count, and the reason is a single heavy task: no
    task can use more than one processor, so a utilisation close to one on a
    single task already forces the bound down.
    """
    return (processors + 1) / 2


def dhall_example():
    """The classic set that global scheduling misses deadlines on."""
    tasks = [task_model.Task("light1", 1, 100), task_model.Task("light2", 1, 100),
             task_model.Task("heavy", 99, 100)]
    trace = task_model.simulate(tasks, "EDF", horizon=100)
    return {"utilisation": float(task_model.utilisation(tasks)),
            "processors": 2, "misses": bool(trace["missed"]),
            "tasks": tasks}
