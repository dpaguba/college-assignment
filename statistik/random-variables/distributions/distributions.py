"""Random variables and their distribution functions.

A random variable attaches a number to each outcome, and its distribution
function is the probability of not exceeding a point. For a discrete variable
that function is a staircase, right continuous with a jump at each value, and
the size of the jump is the probability of that value. The fifth sheet builds
one for a die whose faces read 1, 3, 3, 4, 4, 6.
"""


class Discrete:
    """A discrete random variable, given by the probability of each value."""

    def __init__(self, weights):
        """A variable with the given probability for each value."""
        self.weights = dict(weights)

    def support(self):
        """The values with positive probability, in order."""
        return sorted(value for value, weight in self.weights.items() if weight)

    def probability(self, value):
        """The probability of one value."""
        return self.weights.get(value, 0.0)

    def cdf(self, point):
        """The probability of not exceeding the point."""
        return sum(weight for value, weight in self.weights.items()
                   if value <= point)

    def quantile(self, share):
        """The smallest value whose cumulative probability reaches the share."""
        for value in self.support():
            if self.cdf(value) >= share:
                return value
        return self.support()[-1]


class Continuous:
    """A continuous random variable, given by a density on an interval."""

    def __init__(self, density, low, high, steps=20000):
        """A variable with the given density on the given support."""
        self.density = density
        self.low = low
        self.high = high
        self.steps = steps

    def integral(self, start, end):
        """The probability of falling in an interval, by the trapezium rule."""
        if end <= start:
            return 0.0
        width = (end - start) / self.steps
        total = (self.density(start) + self.density(end)) / 2
        for step in range(1, self.steps):
            total += self.density(start + step * width)
        return total * width

    def cdf(self, point):
        """The probability of not exceeding the point."""
        if point <= self.low:
            return 0.0
        if point >= self.high:
            return 1.0
        return self.integral(self.low, point)
