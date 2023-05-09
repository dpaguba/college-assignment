"""Interval partitioning: the fewest rooms that hold every lecture."""

from __future__ import annotations

import heapq

def maximum_overlap(intervals):
    """The largest number of intervals active at one moment.

    This is the **depth** of the set, and it is a lower bound on the number of
    rooms: if three lectures run at eleven o'clock, no arrangement fits them
    into two rooms. Lower bounds like this are how greedy algorithms are proved
    optimal without an exchange argument.

    Ends are processed before starts at the same instant, so a room that frees
    up exactly when the next interval begins counts as available.
    """
    events = []
    for start, end in intervals:
        events.append((start, 1))
        events.append((end, -1))
    events.sort(key=lambda event: (event[0], event[1]))

    active = busiest = 0
    for _, change in events:
        active += change
        busiest = max(busiest, active)
    return busiest

def partition(intervals):
    """Assign every interval to a room, using as few rooms as possible.

    Sort by start time, and put each lecture in any room that is free; open a
    new one only when none is.

    The proof is the neat part. When a new room is opened, it is because every
    existing room is busy, and each of those rooms is busy with a lecture that
    started earlier and has not finished. So at that instant there are as many
    overlapping lectures as there are rooms, which means the room count never
    exceeds the depth. The depth is a lower bound, so greedy is exactly optimal.

    No exchange argument, no case analysis: the algorithm and the bound meet.
    That is the cleanest optimality proof among the greedy algorithms here.

    A heap over the rooms' finishing times makes "is any room free" one
    comparison, giving O(n log n).
    """
    if not intervals:
        return []

    rooms: list = []
    free_at: list = []

    for start, end in sorted(intervals):
        if free_at and free_at[0][0] <= start:
            _, index = heapq.heappop(free_at)
            rooms[index].append((start, end))
            heapq.heappush(free_at, (end, index))
        else:
            rooms.append([(start, end)])
            heapq.heappush(free_at, (end, len(rooms) - 1))

    return rooms
