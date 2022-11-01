"""Design space exploration: enumerate, filter, and keep the front.

A configuration is a choice of parameters, the space is their product, and
the interesting part is that most of it can be discarded. Constraints remove
what is infeasible and the Pareto front removes what is dominated, and what
remains is the set a designer actually has to choose between.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "evaluation", "pareto-fronts"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "hardware", "power-and-energy"))
import pareto_fronts
import power_and_energy


def explore(frequencies, memories):
    """Every configuration, with its energy and its execution time."""
    space = []
    for frequency in frequencies:
        for memory in memories:
            time = power_and_energy.execution_time(frequency, 3e6) \
                * (1 + 1.0 / memory)
            energy = power_and_energy.energy_per_period(frequency, 3e6) \
                + 2.0 * memory
            space.append({"frequency": frequency, "memory": memory,
                          "time": time, "energy": energy})
    return space


def pareto(space):
    """The undominated configurations, minimising both time and energy."""
    points = [(item["time"], item["energy"]) for item in space]
    front = pareto_fronts.front(points)
    return [item for item in space if (item["time"], item["energy"]) in front]


def filter_feasible(space, max_energy=None, max_time=None):
    """The configurations satisfying the constraints."""
    result = []
    for item in space:
        if max_energy is not None and item["energy"] > max_energy:
            continue
        if max_time is not None and item["time"] > max_time:
            continue
        result.append(item)
    return result
