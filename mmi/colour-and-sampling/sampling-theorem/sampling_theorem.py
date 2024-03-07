"""Sampling and the Nyquist theorem, demonstrated rather than asserted.

    A signal band-limited to f_max is fully determined by samples taken at a
    rate above 2 * f_max, and can be reconstructed exactly.

Below that rate the reconstruction is not merely worse, it is **wrong**: a
frequency above half the sampling rate comes back as a different, lower
frequency, and nothing in the samples reveals that this happened. That is
aliasing, and it is why the theorem is a hard boundary rather than a quality
guideline.
"""

from __future__ import annotations

import cmath
import math


def sample(signal, rate, duration):
    """Take samples of a function at a fixed rate."""
    count = int(duration * rate)
    return [(index / rate, signal(index / rate)) for index in range(count)]


def sine(frequency, amplitude=1.0, phase=0.0):
    """A sine wave as a function of time."""
    return lambda time: amplitude * math.sin(2 * math.pi * frequency * time + phase)


def alias_frequency(frequency, rate):
    """The frequency an under-sampled sine appears to have.

    Everything above half the sampling rate folds back into the band below it.
    A 900 Hz tone sampled at 1000 Hz is indistinguishable from a 100 Hz tone,
    which is the wagon-wheel effect and the reason cameras and audio inputs
    filter before they sample rather than after.
    """
    folded = frequency % rate
    return folded if folded <= rate / 2 else rate - folded


def is_aliased(frequency, rate):
    """Whether a frequency survives this sampling rate."""
    return frequency >= rate / 2


def reconstruct(samples, rate, time):
    """Whittaker-Shannon reconstruction: sum of sincs, one per sample.

    The theorem is constructive, and this is the construction. Each sample
    contributes a sinc centred on it, and the sum is exact for a band-limited
    signal given infinitely many samples. With finitely many it is exact in the
    middle and rings at the ends, which is the truncation and not the theorem.
    """
    total = 0.0
    for index, (_, value) in enumerate(samples):
        argument = math.pi * (rate * time - index)
        weight = 1.0 if abs(argument) < 1e-12 else math.sin(argument) / argument
        total += value * weight
    return total


def reconstruction_error(frequency, rate, duration=1.0, probes=200):
    """How far the reconstruction is from the original, sampled densely.

    The middle of the interval is measured, away from the ends, so the number
    reports the theorem rather than the truncation ringing.
    """
    signal = sine(frequency)
    samples = sample(signal, rate, duration)

    worst = 0.0
    for index in range(probes):
        time = duration * (0.25 + 0.5 * index / probes)
        worst = max(worst, abs(signal(time) - reconstruct(samples, rate, time)))

    return worst


def demonstrate_aliasing(frequencies, rate, duration=1.0):
    """For each frequency, report whether it survives and what it becomes."""
    rows = []
    for frequency in frequencies:
        rows.append({
            "frequency": frequency,
            "rate": rate,
            "aliased": is_aliased(frequency, rate),
            "appears as": alias_frequency(frequency, rate),
            "reconstruction error": round(reconstruction_error(frequency, rate, duration), 4),
        })
    return rows


def nyquist_rate(frequency):
    """The lowest sampling rate that captures a frequency, which is strictly above 2f."""
    return 2 * frequency


def spectrum(samples):
    """The discrete Fourier transform of the sampled values.

    Included here rather than in [fourier-transform](../../image-processing/fourier-transform/)
    because the spectrum is what makes aliasing visible: the folded copy shows
    up as a peak at the wrong place, and the samples alone never do.
    """
    values = [value for _, value in samples]
    count = len(values)

    return [sum(values[index] * cmath.exp(-2j * cmath.pi * frequency * index / count)
                for index in range(count))
            for frequency in range(count)]


def dominant_frequency(samples, rate):
    """The frequency with the largest spectral magnitude, ignoring the constant term."""
    values = spectrum(samples)
    count = len(values)
    half = count // 2

    best = max(range(1, half), key=lambda index: abs(values[index]))
    return best * rate / count
