"""Energy aware scheduling: use the slack, do not waste it.

A task that has to finish by a deadline and has slack can run slower. The
dynamic energy grows with the square of the frequency for a fixed amount of
work, so stretching the execution to fill the deadline is the standard
saving, and the optimum uses all of the slack and no more.

The static power puts a floor under it, and the floor is high enough to
overturn the rule. On the exam's processor, stretching a task with 3 million
cycles over a 100 millisecond deadline means running at 30 MHz and spending
0.405 millijoules, while the optimum runs at 100 MHz and spends 0.18, and
even running flat out at 200 MHz costs only 0.3. Filling the slack is the
worst of the three.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "hardware", "power-and-energy"))
import power_and_energy


def stretch(cycles, deadline, low=10.0, high=200.0):
    """The lowest frequency meeting the deadline, and what it saves."""
    needed = cycles / (deadline * 1e6)
    if needed > high:
        return None
    chosen = max(low, needed)
    return {"chosen frequency": chosen,
            "energy at the slower speed": power_and_energy.energy_per_period(
                chosen, cycles),
            "energy at full speed": power_and_energy.energy_per_period(
                high, cycles),
            "dynamic energy at the slower speed":
                power_and_energy.dynamic_energy(chosen, cycles),
            "dynamic energy at full speed":
                power_and_energy.dynamic_energy(high, cycles),
            "energy at the optimum": power_and_energy.energy_per_period(
                power_and_energy.optimal_frequency(cycles, deadline), cycles),
            "slack used": deadline - power_and_energy.execution_time(chosen,
                                                                     cycles)}


def energy_ratio(slow, fast, dynamic_only=False):
    """How much more the faster frequency costs for the same work.

    The dynamic part scales with the square of the frequency, so doubling it
    costs four times as much switching energy. The total does not, because
    the static draw is paid for a shorter time, and on the exam's processor
    the total ratio is 1.67 rather than 4.
    """
    cycles = 3e6
    if dynamic_only:
        return (power_and_energy.dynamic_energy(fast, cycles)
                / power_and_energy.dynamic_energy(slow, cycles))
    return (power_and_energy.energy_per_period(fast, cycles)
            / power_and_energy.energy_per_period(slow, cycles))


def with_static_power(cycles, deadline, static):
    """The optimum when idling still draws power.

    With a constant draw the slowest frequency stops being optimal, because
    the extra time costs more than the saved dynamic energy. The turning
    point is where the two derivatives meet, and it moves upwards as the
    static power grows.
    """
    best, best_energy = None, None
    steps = 2000
    for index in range(steps + 1):
        frequency = 10.0 + 190.0 * index / steps
        time = power_and_energy.execution_time(frequency, cycles)
        if time > deadline:
            continue
        energy = power_and_energy.energy_per_period(frequency, cycles) \
            + static * (deadline - time) * 1000
        if best_energy is None or energy < best_energy:
            best, best_energy = frequency, energy
    return {"frequency": best, "energy": best_energy}
