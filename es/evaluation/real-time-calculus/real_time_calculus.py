"""Real-time calculus: curves instead of traces.

An arrival curve bounds how many events can arrive in any interval of a given
length, over all positions of that interval. That quantifier is the whole
idea: a trace says what happened, a curve says what can happen, so a bound
derived from it holds for every execution rather than for the one observed.

The exam's stream has two events at every period and one more at 0.3 of the
way through. Its upper curve jumps to 2 immediately, because two events can
arrive at the same instant, and its lower curve stays at 0 until a full
period has passed, because an interval can be placed to miss everything.
"""


def exam_trace(period, repetitions=6):
    """The arrival times of the exam's stream."""
    times = []
    for index in range(repetitions):
        times.append(index * period)
        times.append(index * period)
        times.append(index * period + 0.3 * period)
    return sorted(times)


def upper_arrival_curve(trace, period, samples=400):
    """The largest number of arrivals in any interval of the given length.

    The maximum is taken over the starting point, which is why the curve
    jumps at zero: an interval of any positive length can be placed to cover
    the two simultaneous events.
    """
    def curve(delta):
        """The bound for intervals of length delta."""
        if delta <= 0:
            return 0
        best = 0
        for start in trace:
            for offset in (-1e-9, 0.0):
                begin = start + offset
                count = sum(1 for point in trace
                            if begin <= point < begin + delta)
                best = max(best, count)
        return best
    return curve


def lower_arrival_curve(trace, period, samples=400):
    """The smallest number of arrivals in any interval of the given length."""
    def curve(delta):
        """The bound for intervals of length delta."""
        if delta <= 0:
            return 0
        worst = None
        limit = max(trace) - delta
        step = period / 20.0
        start = 0.0
        while start <= max(limit, 0.0) + 1e-9:
            count = sum(1 for point in trace if start <= point < start + delta)
            worst = count if worst is None else min(worst, count)
            start += step
        return 0 if worst is None else worst
    return curve


def delay_bound(arrival, service, horizon=50.0, step=0.01):
    """The horizontal distance between the curves, which bounds the delay.

    The largest time an event can wait is the longest horizontal gap: the
    time until the service curve reaches the level the arrival curve has
    already produced. When the arrival rate exceeds the service rate the gap
    grows without limit, and the function reports that there is no bound
    rather than returning the largest value inside the horizon.
    """
    if arrival(horizon) > service(horizon):
        return None
    largest = 0.0
    delta = 0.0
    while delta <= horizon:
        needed = arrival(delta)
        wait = 0.0
        while wait <= horizon:
            if service(delta + wait) >= needed:
                break
            wait += step
        else:
            return None
        largest = max(largest, wait)
        delta += step * 10
    return largest


def backlog_bound(arrival, service, horizon=50.0, step=0.01):
    """The vertical distance between the curves, which bounds the buffer."""
    largest = 0.0
    delta = 0.0
    while delta <= horizon:
        largest = max(largest, arrival(delta) - service(delta))
        delta += step
    return largest


def periodic_curve(period, jitter=0.0):
    """The upper arrival curve of a periodic stream with jitter."""
    import math

    def curve(delta):
        """The bound for intervals of length delta."""
        if delta <= 0:
            return 0
        return math.ceil((delta + jitter) / period)
    return curve
