"""Aperiodic jobs: one arrival each, and the rules that order them.

With all jobs available at once, ordering by deadline minimises the maximum
lateness. That is Jackson's rule, and the module checks it by comparing
against every permutation rather than citing it.

With arrival times, the same idea becomes earliest deadline first, which is
optimal only if preemption is allowed. Without preemption a job that starts
early can block one that arrives later with a tighter deadline, and the
module includes a set where exactly that happens.
"""

import itertools


class Job:
    """One aperiodic job with a cost, a deadline and an arrival time."""

    def __init__(self, name, cost, deadline, arrival=0):
        """A job that becomes ready at its arrival time."""
        self.name = name
        self.cost = cost
        self.deadline = deadline
        self.arrival = arrival

    def __repr__(self):
        """The job in the notation of the exam."""
        return "%s(C=%s, d=%s)" % (self.name, self.cost, self.deadline)


def earliest_due_date(jobs):
    """Jackson's rule: run the jobs in order of their deadlines."""
    order = sorted(jobs, key=lambda job: (job.deadline, job.name))
    return _run(order)


def _run(order):
    """Runs the jobs one after another and records the completions."""
    now = 0
    completions = {}
    late = []
    lateness = None
    for job in order:
        now += job.cost
        completions[job.name] = now
        value = now - job.deadline
        lateness = value if lateness is None else max(lateness, value)
        if value > 0:
            late.append(job.name)
    return {"order": order, "completions": completions, "late": late,
            "feasible": not late, "lateness": lateness}


def best_lateness_by_search(jobs):
    """The smallest maximum lateness over every order, by brute force.

    The independent check on Jackson's rule: if the rule is optimal, no
    permutation can do better, and trying them all is the only way to see
    that without the proof.
    """
    best = None
    for order in itertools.permutations(jobs):
        value = _run(list(order))["lateness"]
        best = value if best is None else min(best, value)
    return best


def earliest_deadline_first(jobs):
    """Preemptive scheduling by deadline, with arrival times."""
    remaining = {job.name: job.cost for job in jobs}
    completions = {}
    late = []
    horizon = max(job.deadline for job in jobs) + sum(job.cost for job in jobs)
    for now in range(horizon):
        ready = [job for job in jobs
                 if job.arrival <= now and remaining[job.name] > 0]
        if not ready:
            continue
        chosen = min(ready, key=lambda job: (job.deadline, job.name))
        remaining[chosen.name] -= 1
        if remaining[chosen.name] == 0:
            completions[chosen.name] = now + 1
            if now + 1 > chosen.deadline:
                late.append(chosen.name)
    return {"completions": completions, "late": late, "feasible": not late}


def non_preemptive(jobs):
    """The same policy without preemption, which is no longer optimal."""
    remaining = sorted(jobs, key=lambda job: (job.arrival, job.deadline,
                                              job.name))
    now = 0
    completions = {}
    late = []
    pending = list(remaining)
    while pending:
        ready = [job for job in pending if job.arrival <= now]
        if not ready:
            now = min(job.arrival for job in pending)
            continue
        chosen = min(ready, key=lambda job: (job.deadline, job.name))
        now += chosen.cost
        completions[chosen.name] = now
        if now > chosen.deadline:
            late.append(chosen.name)
        pending.remove(chosen)
    return {"completions": completions, "late": late, "feasible": not late}
