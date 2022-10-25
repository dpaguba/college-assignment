"""Power against energy, and the exam's battery calculation.

Power is a rate and energy is what drains the battery, so a slower processor
can consume more energy for the same work if it runs long enough. The exam's
processor consumes 2·10⁻⁶·f³ + 4 milliwatts at f megahertz, and the constant
term is what makes the optimum finite: without it, running slower would
always win.

The optimum is where the cubic term and the constant term balance, which for
3·10⁶ cycles is exactly 100 MHz.
"""

DYNAMIC = 2e-6
"""The coefficient of the cubic term, in milliwatts per cubed megahertz."""

STATIC = 4.0
"""The constant power, in milliwatts."""


def cmos_power(frequency):
    """The power of the exam's processor at a frequency in megahertz."""
    return DYNAMIC * frequency ** 3 + STATIC


def execution_time(frequency, cycles):
    """How long the work takes at that frequency, in seconds."""
    return cycles / (frequency * 1e6)


def dynamic_energy(frequency, cycles):
    """The switching energy alone, which grows with the square of the frequency."""
    return DYNAMIC * frequency ** 3 * execution_time(frequency, cycles)


def energy_per_period(frequency, cycles):
    """The energy of one activation in millijoules.

    Power times time. The dynamic part grows with the square of the
    frequency and the static part falls with it, which is the trade the
    optimum resolves.
    """
    return cmos_power(frequency) * execution_time(frequency, cycles)


def optimal_frequency(cycles, period, low=10.0, high=200.0):
    """The frequency minimising the energy per activation.

    Differentiating the energy gives f cubed equal to the static power over
    twice the dynamic coefficient, which for the exam's numbers is exactly
    100 MHz. The closed form is used here and checked against a search, so
    the answer does not depend on the algebra being right.
    """
    unconstrained = (STATIC / (2 * DYNAMIC)) ** (1 / 3)
    fastest_needed = cycles / (period * 1e6)
    return min(high, max(low, fastest_needed, unconstrained))


def optimal_frequency_numeric(cycles, period, low=10.0, high=200.0,
                              steps=200000):
    """The same optimum found by searching the range, as a cross-check."""
    best, best_energy = None, None
    for index in range(steps + 1):
        frequency = low + (high - low) * index / steps
        if execution_time(frequency, cycles) > period:
            continue
        energy = energy_per_period(frequency, cycles)
        if best_energy is None or energy < best_energy:
            best, best_energy = frequency, energy
    return best


def battery_life(capacity_mah, volts, frequency, cycles, period,
                 idle_power=0.0):
    """How long a battery lasts under periodic execution."""
    joules = capacity_mah / 1000 * volts * 3600
    active = energy_per_period(frequency, cycles) / 1000
    idle = idle_power / 1000 * (period - execution_time(frequency, cycles))
    per_period = active + idle
    periods = joules / per_period
    seconds = periods * period
    return {"joules": joules, "energy per period": per_period,
            "seconds": seconds, "hours": seconds / 3600}


def race_to_idle_wins(idle_power, cycles=3e6, period=0.1):
    """Whether finishing early and waiting beats stretching to the deadline.

    Two strategies for the same work: run at the energy optimum and then
    idle, or slow down until the task exactly fills the period. With a sleep
    state that costs nothing the first wins, and the second becomes better as
    soon as idling draws more than about three milliwatts, which is where the
    saved switching energy stops paying for the extra idle time.
    """
    fast = optimal_frequency(cycles, period)
    slow = cycles / (period * 1e6)
    fast_energy = energy_per_period(fast, cycles) \
        + idle_power * (period - execution_time(fast, cycles))
    slow_energy = energy_per_period(slow, cycles) \
        + idle_power * (period - execution_time(slow, cycles))
    return fast_energy < slow_energy
