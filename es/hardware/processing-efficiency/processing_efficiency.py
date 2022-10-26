"""Efficiency against flexibility, and the memory wall.

The lecture's central table: the energy per operation falls by orders of
magnitude from a general purpose processor to an application specific
circuit, and the flexibility falls with it. The product is roughly constant,
which is the shape of the trade rather than a law, and it is why an embedded
design picks a point on the curve rather than a technology.

The memory wall is the other half. Processor speed grew faster than memory
speed for decades, so the gap widened, and every technique in the hardware
chapter is an answer to it.
"""

ENERGY_PER_OPERATION = {"ASIC": 1.0, "FPGA": 30.0, "DSP": 200.0,
                        "general purpose": 1000.0}
"""Relative energy per operation, with the circuit as the unit."""

FLEXIBILITY = {"ASIC": 1.0, "FPGA": 100.0, "DSP": 500.0,
               "general purpose": 1000.0}
"""Relative flexibility, on the same scale."""


def energy_per_operation():
    """The energy ordering of the lecture."""
    return dict(ENERGY_PER_OPERATION)


def flexibility(technology):
    """How much a technology can be changed after it is built."""
    if technology not in FLEXIBILITY:
        raise ValueError("unknown technology: %s" % technology)
    return FLEXIBILITY[technology]


def trade_off_spread():
    """How far the efficiency times flexibility product varies."""
    products = [ENERGY_PER_OPERATION[name] / FLEXIBILITY[name]
                for name in ENERGY_PER_OPERATION]
    return max(products) / min(products)


def trade_off_holds(tolerance=4.0):
    """Whether the product stays within the given factor.

    It holds within a factor of 3.33 on the lecture's numbers, so the trade
    is a shape rather than a law: the two extremes sit at one and the
    programmable middle is about three times more efficient than the
    interpolation would suggest.
    """
    products = [ENERGY_PER_OPERATION[name] / FLEXIBILITY[name]
                for name in ENERGY_PER_OPERATION]
    return max(products) / min(products) <= tolerance


def memory_wall(years, processor_growth=1.5, memory_growth=1.07):
    """How the gap between processor and memory speed grows.

    Both improve, and the exponents differ, so the ratio grows exponentially
    even though nothing gets slower. That is the whole argument, and it is
    why caches, prefetching and scratchpads exist.
    """
    before = 1.0
    after = (processor_growth ** years) / (memory_growth ** years)
    return {"ratio before": before, "ratio after": after, "years": years}


def scratchpad_versus_cache():
    """Why an embedded design often prefers a scratchpad to a cache.

    A cache decides at run time and is therefore fast on average and hard to
    bound. A scratchpad is allocated by the compiler, so the worst case is
    known, which is what a real-time analysis needs.
    """
    return {"cache": {"average": "better", "worst case": "hard to bound"},
            "scratchpad": {"average": "worse", "worst case": "known"}}
