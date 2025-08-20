"""Power, energy, and the trade between them.

Dynamic power in CMOS is

    P = C * V^2 * f

so it is linear in the frequency and **quadratic** in the voltage. Since a
higher frequency needs a higher voltage to switch reliably, scaling both
together makes power roughly cubic in the frequency, which is the single fact
behind the end of frequency scaling and the move to multicore.

Energy is power times time, and it is not the same objective. A faster run at
higher power can use less energy than a slower one, or more, and which it is
depends on how much power the chip draws while doing nothing.
"""

from __future__ import annotations


def dynamic_power(capacitance, voltage, frequency):
    """Switching power of a CMOS circuit."""
    return capacitance * voltage ** 2 * frequency


def static_power(leakage_current, voltage):
    """Leakage power, which flows whether the circuit switches or not.

    Negligible in older processes and dominant in modern ones, which is why
    turning parts of a chip off entirely, rather than merely slowing them down,
    became the main lever.
    """
    return leakage_current * voltage


def dvfs_power_ratio(frequency_ratio, voltage_scales=True):
    """Power at a scaled frequency, relative to the original.

    With the voltage scaled proportionally the ratio is cubic, so halving the
    frequency leaves an eighth of the power. Without voltage scaling it is
    merely linear, which is why a frequency cap alone saves so much less than
    people expect.
    """
    if voltage_scales:
        return frequency_ratio ** 3
    return frequency_ratio


def energy(power, seconds):
    """Energy in joules."""
    return power * seconds


def energy_delay(power, seconds):
    """The energy-delay product, which penalises slowness as well as heat.

    Optimising energy alone favours running arbitrarily slowly; optimising
    delay alone favours running arbitrarily hot. The product is the usual
    compromise metric, and it prefers the balanced point: 4 W for 1 s and 1 W
    for 2 s use the same energy, and the second has the better product.
    """
    return energy(power, seconds) * seconds


def race_to_idle(work_seconds, dynamic_power, static_power, speedup, window,
                 idle_power=0.0):
    """Whether finishing quickly and idling beats stretching the work out.

    Racing runs the work at `speedup` times the frequency, which costs
    `speedup^3` times the dynamic power, and then drops to `idle_power` for the
    rest of the window. Crawling stretches the same work across the whole
    window at a lower frequency, which is cheaper dynamically and leaks for the
    entire time.

    The two effects pull in opposite directions and the winner depends on the
    ratio between static and dynamic power. With a small static power crawling
    wins, because the cubic term dominates. With a large one racing wins,
    because leakage is paid per second and racing spends fewer of them. That
    crossover is why the advice changed as leakage grew, and it is why a modern
    chip has deep sleep states rather than only a low-frequency mode.
    """
    racing_time = work_seconds / speedup
    racing = ((dynamic_power * speedup ** 3 + static_power) * racing_time
              + idle_power * max(0.0, window - racing_time))

    ratio = work_seconds / window
    crawling = (dynamic_power * ratio ** 3 + static_power) * window

    return {"race": racing, "crawl": crawling,
            "better": "race" if racing < crawling else "crawl"}


def thermal_design_power(powers, duty_cycles):
    """Average power over a mix of activity levels.

    A chip is cooled for its sustained power, not its peak, which is why a
    processor can exceed its rated power for short bursts. The average over the
    duty cycles is what the cooling has to remove.
    """
    return sum(power * duty for power, duty in zip(powers, duty_cycles))


def temperature(power, thermal_resistance, ambient):
    """Steady-state temperature from a simple thermal resistance model.

    One resistance and one ambient temperature, which is the first-order model
    behind tools such as HotSpot. Its point is that temperature is proportional
    to power, so every power saving is also a thermal one, and the coupling
    runs the other way too: leakage grows with temperature, which is a positive
    feedback loop and the reason thermal runaway is a real failure mode.
    """
    return ambient + power * thermal_resistance
