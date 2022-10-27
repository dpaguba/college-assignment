"""Sampling and conversion: the two exam questions about the analogue edge.

The sampling theorem says a signal can be reconstructed when the sampling
rate is strictly above twice its highest frequency. The exam's case is
exactly at the boundary: a 1000 Hz signal sampled every millisecond gives
1000 samples per second, which is half of what is needed, so the answer is
no.

Under-sampling does not lose the signal quietly. It produces an alias, a
lower frequency that fits the samples exactly, and nothing in the samples
says which of the two was there.
"""


def nyquist_rate(signal_hz):
    """The smallest sampling rate that could suffice."""
    return 2 * signal_hz


def can_reconstruct(signal_hz, sampling_hz):
    """Whether the samples determine the signal.

    Strictly greater, not at least: at exactly twice the frequency a sine can
    be sampled at its zero crossings and vanish entirely.
    """
    return sampling_hz > nyquist_rate(signal_hz)


def alias_frequency(signal_hz, sampling_hz):
    """The frequency an under-sampled signal appears to have."""
    folded = signal_hz % sampling_hz
    if folded > sampling_hz / 2:
        folded = sampling_hz - folded
    return float(folded)


def quantisation_step(range_volts, bits):
    """The size of one step of the converter."""
    return range_volts / (2 ** bits)


def quantisation_error(range_volts, bits):
    """The largest error the conversion can introduce, half a step."""
    return quantisation_step(range_volts, bits) / 2


def converter(kind, bits):
    """The hardware and time cost of the two converters the exam compares."""
    if kind == "flash":
        return {"comparators": 2 ** bits - 1, "steps": 1,
                "note": "one comparator per level, one step"}
    if kind == "successive approximation":
        return {"comparators": 1, "steps": bits,
                "note": "one comparator, one step per bit"}
    raise ValueError("unknown converter: %s" % kind)


def successive_approximation(value, bits):
    """The sequence of approximations the converter produces.

    A binary search over the range: each step decides one bit and halves the
    remaining interval, which is why it needs as many steps as bits and only
    one comparator.
    """
    low, high = 0.0, 1.0
    trace = []
    for _ in range(bits):
        middle = (low + high) / 2
        if value >= middle:
            low = middle
        else:
            high = middle
        trace.append(low)
    return trace
