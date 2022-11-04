"""The task model, and the simulator the rest of the block is checked against.

A real-time task is a cost, a period and a deadline. Three arrival patterns
are distinguished and the difference decides which analysis applies: periodic
tasks arrive exactly every period, sporadic ones at least a period apart, and
aperiodic ones without any bound, so only the first two can be analysed at
all.

The simulator runs a task set for a horizon and reports whether any deadline
was missed. It is slower than any of the analytical tests and it assumes
nothing, which makes it the oracle: a test that says a set is schedulable and
a simulation that misses a deadline cannot both be right.
"""

from fractions import Fraction


class Task:
    """A periodic task with a cost, a period and a deadline."""

    def __init__(self, name, cost, period, deadline=None):
        """A task, with an implicit deadline unless one is given."""
        self.name = name
        self.cost = cost
        self.period = period
        self.deadline = period if deadline is None else deadline

    @property
    def utilisation(self):
        """The share of the processor the task needs."""
        return Fraction(self.cost, self.period)

    @property
    def density(self):
        """The share measured against the deadline rather than the period."""
        return Fraction(self.cost, self.deadline)

    def __repr__(self):
        """The task in the notation the lecture uses."""
        return "%s(C=%s, T=%s, D=%s)" % (self.name, self.cost, self.period,
                                         self.deadline)


def utilisation(tasks):
    """The total utilisation of a task set."""
    return sum((task.utilisation for task in tasks), Fraction(0))


def hyperperiod(tasks):
    """The least common multiple of the periods."""
    result = 1
    for task in tasks:
        result = result * task.period // _gcd(result, task.period)
    return result


def _gcd(first, second):
    """The greatest common divisor."""
    while second:
        first, second = second, first % second
    return first


def arrival_pattern(kind):
    """What each kind of task promises about its arrivals."""
    patterns = {"periodic": "exactly every T", "sporadic": "at least T apart",
                "aperiodic": "no bound"}
    if kind not in patterns:
        raise ValueError("unknown kind: %s" % kind)
    return patterns[kind]


def priority_order(tasks, policy, time=0, remaining=None):
    """The tasks in the order the policy would run them."""
    if policy == "RM":
        return sorted(tasks, key=lambda task: (task.period, task.name))
    if policy == "DM":
        return sorted(tasks, key=lambda task: (task.deadline, task.name))
    if policy == "EDF":
        return sorted(tasks, key=lambda task: (
            (time // task.period + 1) * task.period
            - (task.period - task.deadline), task.name))
    raise ValueError("unknown policy: %s" % policy)


def simulate(tasks, policy, horizon):
    """Runs the task set for the horizon, one time unit at a time.

    Preemptive, with ties broken by name so a run is reproducible. The result
    records which task ran in each slot and whether any job finished after
    its deadline.
    """
    remaining = {task.name: 0 for task in tasks}
    deadlines = {task.name: 0 for task in tasks}
    timeline = []
    missed = []
    for now in range(horizon):
        for task in tasks:
            if now % task.period == 0:
                remaining[task.name] += task.cost
                deadlines[task.name] = now + task.deadline
        ready = [task for task in tasks if remaining[task.name] > 0]
        if not ready:
            timeline.append(None)
            continue
        if policy == "EDF":
            chosen = min(ready, key=lambda task: (deadlines[task.name],
                                                  task.name))
        else:
            chosen = priority_order(ready, policy)[0]
        remaining[chosen.name] -= 1
        timeline.append(chosen.name)
        for task in tasks:
            if remaining[task.name] > 0 and now + 1 >= deadlines[task.name]:
                missed.append((task.name, now + 1))
    return {"timeline": timeline, "missed": missed}
