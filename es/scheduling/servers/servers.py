"""Servers: giving aperiodic work a budget inside a periodic system.

A periodic task set has no room for an aperiodic request unless something is
reserved for it. A polling server checks for work only at its own period, so
a request arriving just after a poll waits a whole period. A deferrable
server keeps its budget until it is used, which answers immediately and costs
a lower utilisation bound for the rest of the system.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "rtos",
                                "task-model"))
import task_model


def polling(capacity, period, request_at, cost):
    """The response time of a request under a polling server."""
    next_poll = ((request_at // period) + 1) * period
    if cost > capacity:
        raise ValueError("the request exceeds the budget")
    return {"served at": next_poll, "waited": next_poll - request_at,
            "response": next_poll - request_at + cost}


def deferrable(capacity, period, request_at, cost):
    """The response time under a deferrable server, which keeps its budget."""
    if cost > capacity:
        raise ValueError("the request exceeds the budget")
    return {"served at": request_at, "waited": 0, "response": cost}


def served_in_period(capacity, demand):
    """How much work a server can serve in one period."""
    return min(capacity, demand)


def with_server(tasks, capacity, period):
    """The task set with the server added as a periodic task."""
    return list(tasks) + [task_model.Task("server", capacity, period)]


def deferrable_bound(server_utilisation):
    """The utilisation bound for the periodic tasks beside a deferrable server.

    Lower than the ordinary bound, because the server may defer its budget
    and then use it at the worst possible moment, which is the price of the
    better response time.
    """
    import math
    share = server_utilisation
    if share <= 0:
        return 1.0
    return math.log((share + 2) / (2 * share + 1))
