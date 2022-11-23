"""Scaling: two laws that answer two different questions.

Amdahl asks how much faster a fixed problem gets on more processors, and the
answer is bounded by the serial share: with a tenth of the work serial, no
machine beats a speedup of ten, however many processors it has.

Gustafson asks how much more work can be done in the same time, and the
answer grows with the machine, because the parallel part of a larger problem
grows while the serial part usually does not. Neither law is wrong; they
describe different experiments, and quoting one against the other is the
usual confusion.
"""


def amdahl(serial_share, workers):
    """The speedup of a fixed problem on the given number of workers."""
    return 1 / (serial_share + (1 - serial_share) / workers)


def ceiling(serial_share):
    """The speedup no number of workers can exceed."""
    if serial_share == 0:
        return float("inf")
    return 1 / serial_share


def gustafson(serial_share, workers):
    """The speedup when the problem grows with the machine."""
    return serial_share + (1 - serial_share) * workers


def measure(workers, serial_share, work=1.0):
    """A simulated run, to check the law against an execution."""
    serial_time = work * serial_share
    parallel_time = work * (1 - serial_share) / workers
    total = serial_time + parallel_time
    return {"speedup": work / total, "serial time": serial_time,
            "parallel time": parallel_time}


def efficiency(serial_share, workers):
    """The speedup per worker, which falls as workers are added."""
    return amdahl(serial_share, workers) / workers
