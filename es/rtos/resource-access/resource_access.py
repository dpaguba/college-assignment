"""The two resource access protocols, and what each one bounds.

Priority inheritance raises the holder of a resource to the priority of the
task waiting for it, which bounds the blocking by the length of the critical
sections but allows one blocking per resource and does not prevent deadlock.

The priority ceiling protocol gives every resource the priority of the
highest task that may use it and refuses a lock that could lead to a chain.
A task is then blocked at most once, for at most one critical section, and
deadlock becomes impossible.
"""


def blocking_bound(protocol, resources):
    """How many critical sections a task can be blocked for."""
    if protocol == "inheritance":
        return {"critical sections": resources,
                "explanation": "once per resource it may need"}
    if protocol == "ceiling":
        return {"critical sections": 1,
                "explanation": "at most one, whatever the number of resources"}
    if protocol == "none":
        return {"critical sections": None,
                "explanation": "unbounded, since any task may intervene"}
    raise ValueError("unknown protocol: %s" % protocol)


def deadlock_free(protocol):
    """Whether the protocol makes a deadlock impossible."""
    return protocol == "ceiling"


def ceiling_of(resource, users, priorities):
    """The priority ceiling of a resource: the highest priority that may use it."""
    return min(priorities[name] for name in users[resource])


def may_lock(protocol, task, resource, held, users, priorities):
    """Whether a task is allowed to take a resource now.

    Under the ceiling protocol a task may lock only if its priority is
    strictly higher than every ceiling currently held by another task, which
    is the rule that removes both the chained blocking and the deadlock.
    """
    if protocol != "ceiling":
        return resource not in held.values()
    ceilings = [ceiling_of(item, users, priorities)
                for owner, item in held.items() if owner != task]
    return all(priorities[task] < ceiling for ceiling in ceilings)
