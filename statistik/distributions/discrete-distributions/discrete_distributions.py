"""The discrete distributions of chapter eight, and how they relate.

Each answers a different question about the same experiment. The binomial
counts successes in a fixed number of independent draws with replacement; the
hypergeometric counts them without replacement; the geometric counts the
draws until the first success; the Poisson counts events in an interval when
they are rare and independent.

The relations are approximations that the tests measure: the hypergeometric
approaches the binomial when the population is large, and the binomial
approaches the Poisson when the number of trials is large and the chance
small.
"""

import math
from math import comb


def binomial_pmf(trials, chance, successes):
    """The probability of exactly this many successes."""
    if not 0 <= successes <= trials:
        return 0.0
    return (comb(trials, successes) * chance ** successes
            * (1 - chance) ** (trials - successes))


def binomial_cdf(trials, chance, successes):
    """The probability of at most this many."""
    return sum(binomial_pmf(trials, chance, count)
               for count in range(successes + 1))


def binomial_mean(trials, chance):
    """The expectation."""
    return trials * chance


def binomial_variance(trials, chance):
    """The variance, largest at a chance of one half."""
    return trials * chance * (1 - chance)


def hypergeometric_pmf(population, successes_total, draws, successes):
    """The probability of this many successes when drawing without replacement."""
    if successes > draws or successes > successes_total:
        return 0.0
    if draws - successes > population - successes_total:
        return 0.0
    return (comb(successes_total, successes)
            * comb(population - successes_total, draws - successes)
            / comb(population, draws))


def hypergeometric_mean(population, successes_total, draws):
    """The expectation, which is the same as the binomial one."""
    return draws * successes_total / population


def hypergeometric_variance(population, successes_total, draws):
    """The variance, smaller than the binomial one by the finite population factor."""
    share = successes_total / population
    return (draws * share * (1 - share)
            * (population - draws) / (population - 1))


def poisson_pmf(rate, count):
    """The probability of this many events."""
    return rate ** count * math.exp(-rate) / math.factorial(count)


def poisson_mean(rate):
    """The expectation, which is the rate."""
    return rate


def poisson_variance(rate):
    """The variance, which is also the rate."""
    return rate


def geometric_pmf(chance, trials):
    """The probability that the first success comes on this trial."""
    if trials < 1:
        return 0.0
    return (1 - chance) ** (trials - 1) * chance


def geometric_mean(chance):
    """The expected number of trials until the first success."""
    return 1 / chance


def geometric_is_memoryless(chance, tolerance=1e-9):
    """Whether waiting longer does not change what remains to be waited.

    The defining property of the geometric distribution: given that the first
    success has not come in the first m trials, the remaining wait has the
    same distribution as the original. No other discrete distribution on the
    positive integers has it.
    """
    for waited in range(1, 6):
        for further in range(1, 6):
            survived = (1 - chance) ** waited
            joint = (1 - chance) ** (waited + further)
            if abs(joint / survived - (1 - chance) ** further) > tolerance:
                return False
    return True
