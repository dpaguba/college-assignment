"""Discrete event simulation, and the loop that stops the clock.

Events carry a time stamp and are processed in time order, so the simulation
jumps from event to event rather than advancing a clock. Simultaneous events
need a tie-breaking rule, and here it is the insertion order, because
otherwise the result depends on the queue's internals.

An event that schedules another with zero delay never lets the clock advance.
That is Zeno behaviour, the discrete event version of an infinite loop, and
the module raises rather than running forever.
"""

import heapq


class ZenoError(Exception):
    """Raised when the clock cannot advance."""


def run(events):
    """Processes the events in time order and returns their names."""
    queue = []
    for order, (time, name) in enumerate(events):
        heapq.heappush(queue, (time, order, name))
    result = []
    while queue:
        _time, _order, name = heapq.heappop(queue)
        result.append(name)
    return result


def times(events):
    """The times at which the events are processed."""
    queue = []
    for order, (time, name) in enumerate(events):
        heapq.heappush(queue, (time, order, name))
    result = []
    while queue:
        time, _order, _name = heapq.heappop(queue)
        result.append(time)
    return result


def chain(start, steps, delay):
    """An event that schedules the next one, the given number of times."""
    if delay <= 0:
        raise ZenoError("a zero delay loop never advances the clock")
    return [start + index * delay for index in range(steps)]


def merge(first, second):
    """Two event streams merged into one, in time order."""
    return run([(time, name) for time, name in list(first) + list(second)])
