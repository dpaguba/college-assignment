"""Minimising lateness: order jobs on one machine so the worst overrun is smallest."""

from __future__ import annotations


def maximum_lateness(jobs):
    """The worst overrun when the jobs are run in the given order."""
    clock = 0
    worst = 0
    for duration, deadline in jobs:
        clock += duration
        worst = max(worst, clock - deadline)
    return worst


def schedule(jobs):
    """Return an order minimising the maximum lateness, and that lateness.

    One machine, jobs with a duration and a deadline, no gaps allowed. The rule
    is **earliest deadline first**, and the durations are ignored entirely.

    Ignoring the durations is what makes it surprising. Shortest job first is
    the intuitive guess and it is wrong: with jobs (1, 100) and (10, 10),
    running the short one first delays the urgent one past its deadline for a
    lateness of 1, while the reverse order is never late at all.

    The proof is an exchange argument on **inversions**, a pair where a later
    deadline is scheduled before an earlier one. Any schedule with an inversion
    has an adjacent one; swapping that adjacent pair does not increase the
    maximum lateness, because only the two swapped jobs change and the later of
    them finishes no later than before. Repeating the swap removes every
    inversion without making anything worse, and the schedule with no
    inversions is exactly the earliest-deadline-first order.

    Note what the argument does not say: it does not claim nothing is late. It
    claims no order does better. That distinction is where greedy proofs are
    usually misread.
    """
    if not jobs:
        return [], 0

    order = sorted(jobs, key=lambda job: job[1])
    return order, maximum_lateness(order)
