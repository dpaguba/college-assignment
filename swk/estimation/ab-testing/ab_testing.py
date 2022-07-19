"""A/B tests: deciding whether a change did anything, and how easily that fails.

The exercise pairs A/B testing with monitoring, and the pairing is the point:
a metric tells you what happened, an experiment tells you whether your change
caused it.

Everything here is the two-proportion test, because the metric in the exercise
is a conversion rate. Three things are computed, and the third is the one
teams get wrong:

- how big a sample the test needs before it is run
- whether an observed difference is beyond what chance produces
- what repeated peeking at a running test does to that answer
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass


def normal_quantile(probability):
    """The inverse normal distribution, by the Beasley-Springer-Moro approximation.

    Written out rather than imported so the module has no dependencies, and
    accurate to about seven digits over the range any test needs.
    """
    a = (-39.69683028665376, 220.9460984245205, -275.9285104469687,
         138.3577518672690, -30.66479806614716, 2.506628277459239)
    b = (-54.47609879822406, 161.5858368580409, -155.6989798598866,
         66.80131188771972, -13.28068155288572)
    c = (-0.007784894002430293, -0.3223964580411365, -2.400758277161838,
         -2.549732539343734, 4.374664141464968, 2.938163982698783)
    d = (0.007784695709041462, 0.3224671290700398, 2.445134137142996,
         3.754408661907416)

    low, high = 0.02425, 1 - 0.02425

    if probability < low:
        q = math.sqrt(-2 * math.log(probability))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
               ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    if probability > high:
        q = math.sqrt(-2 * math.log(1 - probability))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
                ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)

    q = probability - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
           (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)


def normal_cdf(value):
    """The standard normal cumulative distribution."""
    return 0.5 * (1 + math.erf(value / math.sqrt(2)))


@dataclass(frozen=True)
class Result:
    """The outcome of one comparison."""

    control_rate: float
    variant_rate: float
    lift: float
    z: float
    p_value: float
    significant: bool

    def __str__(self):
        """The rates, the lift and the test statistic in one line."""
        return (f"control {self.control_rate:.3%}, variant {self.variant_rate:.3%}, "
                f"lift {self.lift:+.1%}, z = {self.z:.2f}, p = {self.p_value:.4f}, "
                f"{'significant' if self.significant else 'not significant'}")


def sample_size(baseline, minimum_effect, alpha=0.05, power=0.8):
    """Users needed **per group**, computed before the test is run.

    ``minimum_effect`` is the smallest relative improvement worth detecting.
    Deciding it in advance is what makes the test trustworthy: it fixes how long to
    run before any data can tempt anyone to stop.

    The cost of precision is brutal and worth seeing: halving the effect you
    want to detect roughly quadruples the sample.
    """
    treated = baseline * (1 + minimum_effect)
    pooled = (baseline + treated) / 2

    z_alpha = normal_quantile(1 - alpha / 2)
    z_beta = normal_quantile(power)

    numerator = (z_alpha * math.sqrt(2 * pooled * (1 - pooled))
                 + z_beta * math.sqrt(baseline * (1 - baseline)
                                      + treated * (1 - treated))) ** 2
    denominator = (treated - baseline) ** 2

    return math.ceil(numerator / denominator)


def compare(control_successes, control_total, variant_successes, variant_total, alpha=0.05):
    """The two-proportion z-test on a finished experiment.

    The p-value answers one narrow question: if the change did nothing, how
    often would chance alone produce a difference this large? It is not the
    probability that the change works, and reading it that way is the most
    common mistake made with these numbers.
    """
    if not control_total or not variant_total:
        raise ValueError("both groups need users")

    control_rate = control_successes / control_total
    variant_rate = variant_successes / variant_total

    pooled = (control_successes + variant_successes) / (control_total + variant_total)
    standard_error = math.sqrt(pooled * (1 - pooled) * (1 / control_total + 1 / variant_total))

    if standard_error == 0:
        return Result(control_rate, variant_rate, 0.0, 0.0, 1.0, False)

    z = (variant_rate - control_rate) / standard_error
    p_value = 2 * (1 - normal_cdf(abs(z)))
    lift = (variant_rate - control_rate) / control_rate if control_rate else 0.0

    return Result(control_rate, variant_rate, lift, z, p_value, p_value < alpha)


def confidence_interval(successes, total, confidence=0.95):
    """A Wald interval for one rate.

    Reporting the interval instead of the point estimate is the difference
    between "conversion rose to 12 per cent" and "rose to somewhere between 9
    and 15", which is what the data actually supports.
    """
    rate = successes / total
    z = normal_quantile(1 - (1 - confidence) / 2)
    spread = z * math.sqrt(rate * (1 - rate) / total)
    return max(0.0, rate - spread), min(1.0, rate + spread)


def peeking_error(true_rate, per_group, looks=10, alpha=0.05, runs=2000, seed=20260831):
    """Simulate stopping a test early, whenever it happens to look significant.

    Both groups are given the **same** true rate, so every significant result
    is a false positive. Running the test once and testing at the end gives the
    nominal error rate. Testing repeatedly as data arrives, and stopping at the
    first significant look, gives far more.

    This is the single most expensive mistake in practical A/B testing, and it
    costs nothing to demonstrate: the numbers come out of the same simulation.
    """
    generator = random.Random(seed)
    step = max(1, per_group // looks)

    false_at_end = 0
    false_when_peeking = 0

    for _ in range(runs):
        control = variant = 0
        control_successes = variant_successes = 0
        stopped_early = False

        for look in range(1, looks + 1):
            for _ in range(step):
                control += 1
                variant += 1
                control_successes += generator.random() < true_rate
                variant_successes += generator.random() < true_rate

            if not stopped_early:
                result = compare(control_successes, control, variant_successes, variant, alpha)
                if result.significant:
                    stopped_early = True

        final = compare(control_successes, control, variant_successes, variant, alpha)
        false_at_end += final.significant
        false_when_peeking += stopped_early

    return {
        "false positives testing once at the end": false_at_end / runs,
        f"false positives peeking {looks} times": false_when_peeking / runs,
        "nominal rate": alpha,
    }
