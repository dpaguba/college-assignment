"""The event scheduling engine every discrete event simulation is built on.

Time is data. The engine holds a calendar of future events, takes the
earliest, moves the clock to it and lets it schedule more. Nothing advances
the clock except an event, so a period in which nothing happens costs no
computation at all, which is the reason simulated time and processor time
have nothing to do with each other.

Simultaneous events need a tie-breaking rule, and here it is the insertion
order, because the alternative is a result that depends on the internals of
the queue.
"""

import heapq


class Engine:
    """A future event list with a clock."""

    def __init__(self, horizon=None):
        """An engine, optionally stopping at a point in simulated time."""
        self.horizon = horizon
        self.queue = []
        self.clock = 0.0
        self.counter = 0

    def schedule(self, time, name, handler=None):
        """Puts an event in the calendar.

        An event scheduled by a handler inherits that handler unless it names
        another, which is what lets a recurring event describe itself once.
        """
        if self.horizon is not None and time >= self.horizon:
            return
        heapq.heappush(self.queue, (time, self.counter, name, handler))
        self.counter += 1

    def run(self, limit=100000):
        """Processes the calendar and returns the events in time order."""
        processed = []
        for _ in range(limit):
            if not self.queue:
                return processed
            time, _order, name, handler = heapq.heappop(self.queue)
            self.clock = time
            processed.append((time, name))
            if handler is not None:
                for event in handler(time, name):
                    following = list(event)
                    if len(following) < 3 or following[2] is None:
                        following = list(following[:2]) + [handler]
                    self.schedule(*following)
        return processed
