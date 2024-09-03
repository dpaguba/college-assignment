"""Average memory access time, and what actually improves it.

    AMAT = hit time + miss rate * miss penalty

Three terms, three ways to improve, and they trade against each other: a bigger
cache lowers the miss rate and raises the hit time, and a second level lowers
the penalty and adds its own hit time to every miss.

The formula's value is that it makes the trade arithmetic rather than
intuition. A cache with a 5% miss rate and a 100-cycle penalty spends five
cycles per access on misses and one on hits, so the memory is five times more
important than the cache, which is not what the hit rate of 95% suggests.
"""

from __future__ import annotations


def amat(hit_time, miss_rate, miss_penalty):
    """Average access time of a single-level cache."""
    return hit_time + miss_rate * miss_penalty


def multilevel(levels, memory_penalty):
    """Average access time of a hierarchy, from the outside in.

    Each level is a hit time and a **local** miss rate, the fraction of the
    accesses reaching that level that miss it. The penalty of a level is the
    access time of everything below it, which is what makes the recursion the
    natural formulation.
    """
    penalty = memory_penalty

    for hit_time, miss_rate in reversed(levels[1:]):
        penalty = hit_time + miss_rate * penalty

    hit_time, miss_rate = levels[0]
    return hit_time + miss_rate * penalty


def global_miss_rate(local_rates):
    """The fraction of all accesses that reach memory.

    The product of the local rates, and the number that matters for bandwidth.
    A second-level cache with a 40% local miss rate sounds bad and, behind a
    first level missing 5% of the time, lets only 2% of accesses through.
    """
    product = 1.0
    for rate in local_rates:
        product *= rate
    return product


def memory_cpi(miss_rate, miss_penalty, accesses_per_instruction=1.0):
    """The memory contribution to the CPI.

    More than one access per instruction is the normal case: every instruction
    is fetched and some also load or store, so the factor is above one and
    often near 1.3. Leaving it out understates the memory cost by a third.
    """
    return accesses_per_instruction * miss_rate * miss_penalty


def compare_improvements(hit_time, miss_rate, miss_penalty):
    """Which of three equal-looking improvements helps most.

    Halving the miss rate and halving the penalty give **exactly** the same
    answer, since they are the two factors of one product. The hit time is what
    breaks the symmetry: it is paid on every access rather than only on misses,
    so halving it is worth less whenever the miss cost dominates and more when
    it does not.

    The table is the answer to "where should the next transistor go", and it
    depends entirely on the starting point.
    """
    base = amat(hit_time, miss_rate, miss_penalty)

    return {
        "base": base,
        "half miss rate": amat(hit_time, miss_rate / 2, miss_penalty),
        "half penalty": amat(hit_time, miss_rate, miss_penalty / 2),
        "half hit time": amat(hit_time / 2, miss_rate, miss_penalty),
    }
