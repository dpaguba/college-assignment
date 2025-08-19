"""Execution time, CPI, and why single numbers mislead.

The iron law of performance:

    time = instructions * cycles per instruction / clock rate

Every architectural change moves one of the three, usually at the expense of
another. A richer instruction set lowers the count and raises the CPI; a deeper
pipeline raises the clock and the branch penalty. Comparing designs means
comparing the product, which is why the law is worth writing down.
"""

from __future__ import annotations

import math


def execution_time(instructions, cpi, clock_hz):
    """Run time in seconds, from the three factors."""
    return instructions * cpi / clock_hz


def average_cpi(mix):
    """CPI of a program from its instruction mix.

    A mix entry is a class name, its share of the instructions, and the cycles
    that class takes. The average is weighted by the share, which is the only
    sense in which a machine has "a" CPI: it depends on the program.
    """
    return sum(share * cycles for _, share, cycles in mix)


def improve(mix, name, factor):
    """Speed up one instruction class by a factor."""
    return [(entry, share, cycles / factor if entry == name else cycles)
            for entry, share, cycles in mix]


def speedup(before, after):
    """Speedup from a change to the instruction mix, at equal counts."""
    return average_cpi(before) / average_cpi(after)


def mips(instructions, seconds):
    """Millions of instructions per second.

    Reported because it is famous, not because it is useful. MIPS says nothing
    about the work done, so a machine whose instructions do less can win on it
    while losing on run time. The test in this module shows exactly that case:
    2 MIPS at 1.0 seconds against 1.11 MIPS at 0.9 seconds, where the second
    machine finishes first.
    """
    return instructions / (seconds * 10 ** 6)


def geometric_mean(ratios):
    """The right average for normalised ratios.

    The arithmetic mean of speedups depends on which machine is the baseline,
    so two people can average the same measurements and rank the machines
    differently. The geometric mean does not, which is why SPEC uses it.
    """
    product = 1.0
    for value in ratios:
        product *= value
    return product ** (1.0 / len(ratios))


def arithmetic_mean(values):
    """The right average for times, and the wrong one for ratios."""
    return sum(values) / len(values)


def harmonic_mean(rates):
    """The right average for rates, such as instructions per second."""
    return len(rates) / sum(1.0 / rate for rate in rates)


def clock_change(cpi, clock_hz, new_cpi, new_clock_hz, instructions=1.0):
    """Whether a design change is a win, given both effects.

    The usual trade: a higher clock costs a higher CPI, through a deeper
    pipeline or a slower memory in cycles. Only the product decides, and the
    function returns it rather than either factor.
    """
    before = execution_time(instructions, cpi, clock_hz)
    after = execution_time(instructions, new_cpi, new_clock_hz)
    return {"before": before, "after": after, "speedup": before / after}
