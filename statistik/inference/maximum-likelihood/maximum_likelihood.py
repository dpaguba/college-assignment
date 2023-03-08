"""Maximum likelihood: the parameter under which the data was most likely.

The recipe is the same every time. Write the likelihood of the observed
sample as a function of the parameter, take the logarithm because the
likelihood is a product, differentiate, and set the derivative to zero. The
seventh sheet asks for it for the standard deviation of a normal
distribution, and the answer is the root mean squared deviation.

The estimator is not automatically unbiased. With the mean estimated from the
same data, the maximum likelihood estimator of the variance divides by n and
is exactly the biased one from the estimation module.
"""

import math


def bernoulli(data):
    """The chance of success that makes the observed coin flips most likely."""
    return sum(data) / len(data)


def bernoulli_likelihood(data, chance):
    """The probability of the observed flips under a given chance."""
    successes = sum(data)
    failures = len(data) - successes
    return chance ** successes * (1 - chance) ** failures


def poisson(data):
    """The rate that makes the observed counts most likely."""
    return sum(data) / len(data)


def poisson_score(data, rate):
    """The derivative of the log likelihood, which vanishes at the estimate."""
    return sum(data) / rate - len(data)


def normal_sigma(data, mean=None):
    """The maximum likelihood estimate of the standard deviation.

    With the mean known, this is the root mean squared deviation from it.
    With the mean estimated from the same sample, the same formula uses the
    sample mean and divides by n, which is the biased estimator: the sample
    mean sits closer to the data than the true mean does, so the deviations
    come out too small.
    """
    size = len(data)
    centre = sum(data) / size if mean is None else mean
    return math.sqrt(sum((value - centre) ** 2 for value in data) / size)


def normal_log_likelihood(data, mean, sigma):
    """The log likelihood of a sample under a normal distribution."""
    size = len(data)
    total = sum((value - mean) ** 2 for value in data)
    return (-size / 2 * math.log(2 * math.pi) - size * math.log(sigma)
            - total / (2 * sigma ** 2))


def exponential(data):
    """The rate of an exponential distribution, which is the inverse mean."""
    return len(data) / sum(data)
