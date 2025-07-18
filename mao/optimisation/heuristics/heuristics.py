"""Heuristics: an answer without a bound on how good it is.

Local search improves a solution by looking at its neighbours and stops when
none is better, which is a local optimum and need not be the global one. That
is not a flaw to be fixed but the definition of the method, and the module
exhibits a landscape where it happens.

Simulated annealing accepts a worse solution with a probability that falls
over time, so it can leave a local optimum early and settles later. It has no
optimality guarantee either, and the difference from branch and bound is
exactly that: an exact method can report a gap and a heuristic cannot.
"""

import math
import random


def _cost(position):
    """A landscape with a local and a global minimum."""
    return math.sin(position) + 0.1 * (position - 4) ** 2


def local_search(seed=0, start=0.0, step=0.1, limit=1000):
    """Improves while a neighbour is better."""
    generator = random.Random(seed)
    current = start
    initial = _cost(current)
    for _ in range(limit):
        neighbours = [current - step, current + step]
        best = min(neighbours, key=_cost)
        if _cost(best) >= _cost(current):
            break
        current = best
    return {"initial cost": initial, "final cost": _cost(current),
            "position": current}


def local_optimum_cost():
    """The cost of the local optimum the search from zero reaches."""
    return local_search(start=0.0)["final cost"]


def gets_stuck():
    """Whether the search stops somewhere the global optimum is not."""
    local = local_search(start=0.0)
    global_best = min((_cost(index / 100) for index in range(-200, 1000)))
    return local["final cost"] > global_best + 1e-6


def annealing(seed=0, start=0.0, steps=20000, temperature=2.0):
    """Simulated annealing, which may accept a worse solution early."""
    generator = random.Random(seed)
    current = start
    best = current
    for index in range(steps):
        heat = temperature * (1 - index / steps) + 1e-9
        candidate = current + generator.uniform(-0.5, 0.5)
        difference = _cost(candidate) - _cost(current)
        if difference < 0 or generator.random() < math.exp(-difference / heat):
            current = candidate
            if _cost(current) < _cost(best):
                best = current
    return {"cost": _cost(best), "position": best}


def optimality_gap(method):
    """The bound a method can report, or nothing when it has none."""
    bounds = {"branch and bound": "the relaxation bounds the optimum",
              "dynamic programming": "exact by construction",
              "local search": None, "simulated annealing": None,
              "genetic algorithm": None}
    if method not in bounds:
        raise ValueError("unknown method: %s" % method)
    return bounds[method]
