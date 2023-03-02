# Continuous distributions

The sixth sheet asks for the expectation and the variance of the uniform
distribution from the definition. The answers are the midpoint and the width
squared over twelve, and both are checked here in two ways: from the formula
and by numerically integrating the density.

```
uniform on [2, 8]:  mean 5,  variance 3
```

The two agree to five decimals, which is the point of doing both. The formula
is a claim about an integral, and evaluating the integral is the check.

## A density is not a probability

The uniform density on an interval of width one half is 2, which is greater
than one and perfectly correct. Only the integral over an interval is a
probability, and the integral over a single point is zero.

## The exponential distribution

The waiting time at a constant rate. Its expectation is the inverse of the
rate and its variance the square of that, so the standard deviation equals
the mean, which is a large spread and the reason waiting times feel
unpredictable.

It is memoryless, checked across a grid of waiting times: a component that
has survived an hour has the same remaining life as a new one. That is a
strong assumption about the world and the reason the exponential is the wrong
model for anything that ages.
