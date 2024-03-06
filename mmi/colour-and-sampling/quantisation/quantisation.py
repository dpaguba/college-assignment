"""Quantisation: how many levels a value is allowed to take.

Sampling discretises **when** a value is measured; quantisation discretises
**what** it may be. Both are needed to store a signal, and each has its own
failure mode: aliasing for sampling, banding for quantisation.

The lecture's two points are the Mach band effect, which makes a small step
between levels look like a bright edge that is not there, and the difference
between linear and logarithmic level spacing, which follows from perception
being roughly logarithmic.
"""

from __future__ import annotations

import math


def linear_quantise(value, levels, low=0.0, high=1.0):
    """Round a value to one of equally spaced levels.

    Equal spacing wastes levels where the eye cannot see the difference and
    starves the range where it can, which is exactly what logarithmic spacing
    fixes.
    """
    if levels < 2:
        raise ValueError("quantisation needs at least two levels")

    span = high - low
    step = span / (levels - 1)
    index = round((value - low) / step)
    index = max(0, min(levels - 1, index))
    return low + index * step, index


def logarithmic_quantise(value, levels, low=0.001, high=1.0):
    """Round a value to one of logarithmically spaced levels.

    Perception of brightness follows roughly a power law, so equal **ratios**
    look like equal steps, not equal differences. Spacing the levels
    geometrically therefore spends them where they are visible, which is why
    audio and image formats do it.
    """
    if levels < 2:
        raise ValueError("quantisation needs at least two levels")

    value = max(low, min(high, value))
    ratio = math.log(high / low) / (levels - 1)
    index = round(math.log(value / low) / ratio)
    index = max(0, min(levels - 1, index))
    return low * math.exp(index * ratio), index


def quantisation_error(values, levels, method=linear_quantise, **bounds):
    """The largest and the mean error over a set of values."""
    errors = [abs(value - method(value, levels, **bounds)[0]) for value in values]
    return {"levels": levels, "worst": max(errors), "mean": sum(errors) / len(errors)}


def bits_needed(levels):
    """How many bits a number of levels costs, which is what a format pays."""
    return math.ceil(math.log2(levels))


def signal_to_noise(levels):
    """The classic 6 dB per bit rule for uniform quantisation.

    The argument is the number of **levels**, not the number of bits: `n` bits
    give `2^n` levels, so 8 bits means 256 and 48 dB, while passing 8 directly
    describes a 3-bit signal at 18 dB.

    Each extra bit halves the step and so gains about 6 decibels. It is the
    number that decides whether 8 bits per channel are enough, and for smooth
    gradients they are not, which is where banding comes from.
    """
    return 20 * math.log10(levels)


def mach_band_demo(levels, width=32):
    """A ramp quantised into bands, which the eye exaggerates at the edges.

    The values are a straight ramp and the quantised version is a staircase.
    Each step is a genuine discontinuity, and lateral inhibition in the retina
    turns it into a visible bright and dark line at every boundary, which is
    not in the data at all. That is the Mach band effect, and it is the reason
    banding is more objectionable than its numeric error suggests.
    """
    ramp = [index / (width - 1) for index in range(width)]
    banded = [linear_quantise(value, levels)[0] for value in ramp]
    steps = [index for index in range(1, width) if banded[index] != banded[index - 1]]

    return {"ramp": ramp, "quantised": banded, "step positions": steps,
            "step size": 1 / (levels - 1)}


def posterise(image, levels):
    """Quantise every pixel of a greyscale image to a number of levels."""
    return [[linear_quantise(value, levels)[0] for value in row] for row in image]
