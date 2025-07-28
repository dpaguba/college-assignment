"""The warm-up period, and why the start of a run has to be thrown away.

A simulation usually starts empty, which is not a state the system spends much
time in. The early observations are therefore biased downwards for a queue,
and averaging them into the result biases the answer.

Detecting the end of the transient is a judgement, not a computation. The
rule here is the standard one: smooth the trace and take the first point at
which it stops trending, which is Welch's method in its simplest form. It has
no guarantee attached, which is why the lecture treats the warm-up length as
a modelling decision to be justified rather than a number to be computed.
"""


def moving_average(values, window):
    """The trace smoothed over a window."""
    if window > len(values):
        raise ValueError("the window is longer than the trace")
    result = []
    for index in range(len(values) - window + 1):
        result.append(sum(values[index:index + window]) / window)
    return result


def detect(values, window=200, tolerance=0.02):
    """The first point at which the smoothed trace stops rising."""
    smoothed = moving_average(values, window)
    final = sum(smoothed[len(smoothed) // 2:]) / (len(smoothed)
                                                  - len(smoothed) // 2)
    for index, value in enumerate(smoothed):
        if abs(value - final) <= tolerance * max(abs(final), 1e-9):
            return {"cut off": index, "level": final}
    return {"cut off": len(smoothed) // 2, "level": final}


def bias_of_the_start(values, length=200):
    """How far the first observations sit from the long run average."""
    start = sum(values[:length]) / length
    whole = sum(values) / len(values)
    return {"start": start, "whole run": whole, "difference": whole - start}
