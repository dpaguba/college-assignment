"""Amdahl's law, Gustafson's law, and why they disagree.

Both describe the speedup of a parallel program and they answer different
questions. Amdahl fixes the **problem** and asks how much faster more cores
make it. Gustafson fixes the **time** and asks how much bigger a problem the
extra cores allow.

Amdahl's answer is bounded by the serial fraction, however many cores there
are: 4% serial caps the speedup at 25. Gustafson's answer grows without bound,
because the serial part stays constant while the parallel work grows with the
machine.

Neither is wrong. They model different situations, and which one applies is a
question about the workload rather than about the hardware.
"""

from __future__ import annotations


def amdahl(parallel_fraction, cores):
    """Speedup of a fixed problem on more cores.

    The serial part runs at the same speed whatever the machine, so it stops
    being a small share of the runtime and becomes all of it. That is the whole
    content of the law, and it is why the limit is the reciprocal of the serial
    fraction.
    """
    serial = 1.0 - parallel_fraction
    return 1.0 / (serial + parallel_fraction / cores)


def amdahl_limit(parallel_fraction):
    """The best speedup any number of cores can reach."""
    serial = 1.0 - parallel_fraction
    return float("inf") if serial == 0 else 1.0 / serial


def gustafson(parallel_fraction, cores):
    """Speedup when the problem grows with the machine.

    The scaled speedup is `serial + cores * parallel`, which is linear in the
    number of cores. The assumption behind it is that a bigger machine is
    bought to solve a bigger problem, which is true of simulations and false of
    latency-bound work.
    """
    serial = 1.0 - parallel_fraction
    return serial + cores * parallel_fraction


def simulate_runtime(parallel_fraction, cores):
    """Run time of a fixed problem, computed by dividing the work up.

    Deliberately not the formula: the serial work takes its own time and the
    parallel work is split evenly across the cores. Comparing this against
    `amdahl` checks that the law says what the mechanism does, rather than
    checking the law against itself.
    """
    serial = 1.0 - parallel_fraction
    return serial + parallel_fraction / cores


def serial_fraction(sections):
    """The share of runtime that cannot be parallelised at all.

    A section is a name, its share of the runtime, and the maximum number of
    parallel units it can be split into, with `None` for unbounded. A section
    capped at one unit is serial.
    """
    return sum(share for _, share, cap in sections if cap == 1)


def sectioned_speedup(sections, cores):
    """Speedup when different parts have different parallelism limits.

    Amdahl's law with more than two categories. Each section is sped up by the
    smaller of the available cores and its own cap, which is what makes the
    curve flatten in stages rather than at one point: as cores grow, one
    section after another hits its ceiling and stops contributing.
    """
    total = 0.0

    for _, share, cap in sections:
        limit = cores if cap is None else min(cores, cap)
        total += share / limit

    return 1.0 / total


def cores_for_speedup(sections, target, limit=10 ** 7):
    """The smallest number of cores reaching a target speedup, or `None`.

    Searched rather than solved. The closed form exists only while no section
    has hit its cap, and the interesting cases are exactly the ones where one
    has, which is the point of the exercise.
    """
    if sectioned_speedup(sections, limit) < target:
        return None

    low, high = 1, limit
    while low < high:
        middle = (low + high) // 2
        if sectioned_speedup(sections, middle) >= target:
            high = middle
        else:
            low = middle + 1

    return low


def gustafson_scaled(sections, cores, grow):
    """Scaled speedup when some sections solve a larger problem.

    The Gustafson question applied to the sheet's program: with the cores fixed
    at what Amdahl needed, growing the unbounded section means more work in the
    same time, and the speedup relative to running that larger problem serially
    is what the law reports.
    """
    parallel_time = 0.0
    serial_work = 0.0

    for name, share, cap in sections:
        factor = grow.get(name, 1.0)
        work = share * factor
        serial_work += work
        limit = cores if cap is None else min(cores, cap)
        parallel_time += work / limit

    return serial_work / parallel_time


def efficiency(speedup, cores):
    """Speedup per core, which is what a purchase decision actually compares.

    A speedup of 10 on 16 cores is an efficiency of 0.63, and the same speedup
    on 64 cores is 0.16. The second machine is faster and much worse value,
    which the speedup number alone does not say.
    """
    return speedup / cores
