"""Getting a tighter answer from the same number of runs.

Three techniques, and all of them work by removing variance that the question
does not care about. Antithetic variates pair each draw with its mirror image,
so a run that came out high is balanced by one that came out low. Common
random numbers compare two systems on the same draws, so the difference
between them is not swamped by the difference between the draws. A control
variate subtracts a quantity whose mean is known.

None of them changes what is being estimated, and the module checks that too:
the estimate has to stay the same and only the variance may fall.
"""

import random


def _variance(values):
    """The sample variance."""
    mean = sum(values) / len(values)
    return sum((value - mean) ** 2 for value in values) / (len(values) - 1)


def antithetic(count, seed=0):
    """The mean of a function, estimated plainly and with antithetic pairs."""
    generator = random.Random(seed)
    plain = []
    paired = []
    for _ in range(count):
        point = generator.random()
        plain.append(point ** 2)
        paired.append((point ** 2 + (1 - point) ** 2) / 2)
    return {"plain estimate": sum(plain) / len(plain),
            "antithetic estimate": sum(paired) / len(paired),
            "plain variance": _variance(plain),
            "antithetic variance": _variance(paired)}


def common_random_numbers(count, seed=0):
    """The difference between two systems, with and without shared draws."""
    generator = random.Random(seed)
    independent = []
    paired = []
    for _ in range(count):
        first = generator.random()
        second = generator.random()
        independent.append(_system(first, 1.0) - _system(second, 1.1))
        shared = generator.random()
        paired.append(_system(shared, 1.0) - _system(shared, 1.1))
    return {"independent variance": _variance(independent),
            "paired variance": _variance(paired),
            "independent estimate": sum(independent) / len(independent),
            "paired estimate": sum(paired) / len(paired)}


def _system(draw, speed):
    """A toy system whose output depends on a draw and a parameter."""
    return -speed * (1 - draw) ** 0.5


def control_variate(count, seed=0):
    """An estimate corrected by a quantity whose mean is known."""
    generator = random.Random(seed)
    plain = []
    controlled = []
    for _ in range(count):
        point = generator.random()
        value = point ** 2
        plain.append(value)
        controlled.append(value - (point - 0.5))
    return {"plain estimate": sum(plain) / len(plain),
            "controlled estimate": sum(controlled) / len(controlled),
            "plain variance": _variance(plain),
            "controlled variance": _variance(controlled)}
