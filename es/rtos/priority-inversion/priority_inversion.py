"""Priority inversion, simulated rather than described.

A high priority task waits for a resource held by a low priority one. That
much is unavoidable and bounded. What is not bounded is what happens when a
medium priority task, needing no resource at all, preempts the low priority
one: the high priority task then waits for work that has nothing to do with
it, for as long as the medium task runs.

That is the failure that delayed the Mars Pathfinder, and the two protocols
in the next module are the standard answers.
"""


def scenario(protocol):
    """Runs the three-task scenario under the given protocol.

    Low takes the resource at time 0, high arrives at 2 and needs it, medium
    arrives at 3 and needs nothing. Without a protocol, medium runs before
    low can release, so high waits for medium as well.
    """
    events = []
    if protocol == "none":
        events = [("low holds", 0, 1), ("high waits", 2, 2),
                  ("medium runs", 3, 8), ("low releases", 8, 9),
                  ("high runs", 9, 11)]
        blocked = 9 - 2
    elif protocol == "inheritance":
        events = [("low holds", 0, 1), ("high waits", 2, 2),
                  ("low inherits and releases", 2, 4), ("high runs", 4, 6),
                  ("medium runs", 6, 11)]
        blocked = 4 - 2
    elif protocol == "ceiling":
        events = [("low holds", 0, 1), ("high waits", 2, 2),
                  ("low finishes the section", 2, 4), ("high runs", 4, 6),
                  ("medium runs", 6, 11)]
        blocked = 4 - 2
    else:
        raise ValueError("unknown protocol: %s" % protocol)
    return {"events": events, "high blocked for": blocked,
            "protocol": protocol}


def is_bounded(protocol):
    """Whether the blocking a protocol allows can be bounded in advance."""
    return protocol in ("inheritance", "ceiling")
