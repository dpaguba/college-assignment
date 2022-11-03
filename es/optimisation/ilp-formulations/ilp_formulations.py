"""Integer linear programming, and why embedded design keeps reaching for it.

Assignment, scheduling and allocation are all the same shape: choose a
zero-one variable per pair, satisfy some linear constraints, minimise a
linear cost. Writing the problem that way separates the model from the
solver, which is the point of the lecture's ILP session.

The solver here is exhaustive, so it is exact and useless beyond a handful of
tasks. That is the picture worth keeping: the formulation is easy and the solving is
what costs, and the linear relaxation is the standard way to get a bound
without paying for it.
"""

import itertools


def assign(tasks, processors, costs, capacity=None):
    """The cheapest assignment of tasks to processors under the capacities."""
    best, best_cost = None, None
    for choice in itertools.product(processors, repeat=len(tasks)):
        assignment = dict(zip(tasks, choice))
        if capacity is not None:
            counts = {name: 0 for name in processors}
            for processor in choice:
                counts[processor] += 1
            if any(counts[name] > capacity.get(name, len(tasks))
                   for name in processors):
                continue
        total = sum(costs[(task, assignment[task])] for task in tasks)
        if best_cost is None or total < best_cost:
            best, best_cost = assignment, total
    return {"assignment": best, "cost": best_cost}


def relaxation(tasks, processors, costs):
    """The linear relaxation, which allows a task to be split.

    Each task takes its cheapest processor regardless of the capacities, so
    the value is a lower bound on the integer optimum and is reached only
    when the constraints happen not to bind.
    """
    return sum(min(costs[(task, processor)] for processor in processors)
               for task in tasks)


def search_space(tasks, processors):
    """How many assignments there are, which is why the solver matters."""
    return processors ** tasks


def as_constraints(tasks, processors):
    """The constraints of the assignment problem, as text.

    One equality per task saying it is placed exactly once, and one
    inequality per processor for its capacity. Writing them out is the whole
    modelling step, and everything after it is the solver's problem.
    """
    lines = []
    for task in tasks:
        lines.append(" + ".join("x_%s_%s" % (task, processor)
                                for processor in processors) + " = 1")
    for processor in processors:
        lines.append(" + ".join("x_%s_%s" % (task, processor)
                                for task in tasks) + " <= capacity")
    return lines
