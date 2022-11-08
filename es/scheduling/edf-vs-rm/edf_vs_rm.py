"""Static against dynamic priorities, and where each one wins.

Rate monotonic assigns priorities once, from the periods. Earliest deadline
first assigns them at every instant, from the absolute deadlines. The second
uses the processor completely and the first does not, and the second is worse
under overload, because a job that will miss its deadline becomes the most
urgent one and takes the processor from jobs that could still finish.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "rtos",
                                "task-model"))
import task_model


def priority_kind(policy):
    """When the policy assigns priorities."""
    kinds = {"RM": "static", "DM": "static", "EDF": "dynamic",
             "LST": "dynamic"}
    if policy not in kinds:
        raise ValueError("unknown policy: %s" % policy)
    return kinds[policy]


def compare(tasks, horizon):
    """The two policies run on the same set, with the preemptions counted."""
    report = {}
    for policy in ("RM", "EDF"):
        trace = task_model.simulate(tasks, policy, horizon)
        report[policy] = {"missed": trace["missed"],
                          "preemptions": _preemptions(trace["timeline"])}
    return report


def _preemptions(timeline):
    """How often the running task changed while the previous one was unfinished."""
    changes = 0
    for before, after in zip(timeline, timeline[1:]):
        if before is not None and after is not None and before != after:
            changes += 1
    return changes


def overload_behaviour():
    """How the two policies behave when the set does not fit.

    Under overload the dynamic policy keeps running a job that is already
    doomed, because a missed deadline is the most urgent one, and the misses
    cascade. The static policy sheds the lowest priority task and keeps the
    rest, which is the behaviour a designer usually wants.
    """
    tasks = [task_model.Task("t1", 3, 5), task_model.Task("t2", 4, 7),
             task_model.Task("t3", 5, 11)]
    horizon = 77
    rate = task_model.simulate(tasks, "RM", horizon)
    deadline = task_model.simulate(tasks, "EDF", horizon)
    return {"utilisation": float(task_model.utilisation(tasks)),
            "RM misses": len(rate["missed"]),
            "EDF misses": len(deadline["missed"])}
