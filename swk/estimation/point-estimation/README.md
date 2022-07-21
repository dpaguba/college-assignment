# Two-point and three-point estimation

The effort of a work package is a random variable with an unknown density.
The lecture's practical answer: ask for a smallest and a largest value, maybe
a middle one, **assume a distribution**, and compute.

```
E(x) = (a + r*c + b) / (2 + r)        S(x) = (b - a) / u
```

The pair `(r, u)` is the assumption, and the lecture tabulates several:

| Assumption | r | u |
|---|---|---|
| two-point | 0 | 6 |
| PERT (beta approximation) | 4 | 6 |
| beta, quadratic | 4 | 5.29 |
| beta, cubic | 6 | 6 |

## The exercise, computed

The five components of the game project from sheet 2:

| | two-point | three-point |
|---|---|---|
| expected total | **248.00 h** | **250.00 h** |
| standard deviation | 29.01 h | 29.01 h |
| one sigma range | 219 to 277 | 221 to 279 |

The two expectations are close here by accident: the middle values happen to
sit near the midpoints. The deviations are **identical**, and that is not an
accident, it is the formula: `S` depends only on the range, so two estimators
who disagree entirely about the likely value report the same uncertainty. It
is worth knowing before quoting the number as if it measured confidence.

## Why variances add and deviations do not

```
E = sum of Ei          S = sqrt(sum of Si^2)
```

Adding deviations would overstate the risk badly. Five packages of 6 hours
deviation each total 13.4, not 30, which is why a project split into many
small independent packages is proportionally more predictable than one large
one.

That holds **while the packages are independent**. One shared bottleneck
breaks it, and no formula here will notice.

## What the Monte Carlo check found

Sampling each package from a beta-PERT distribution and summing gives a mean
of 249.99 against the formula's 250.00, so the expectation is exact. The
simulated deviation is 32.35 against the formula's 29.01.

The gap is real and expected: `(b - a) / 6` is an approximation that is exact
only when the distribution is symmetric, and three of these five packages are
skewed. The formula understates the spread by about ten per cent here, which
is the direction that matters for a plan.

The simulation also answers what the formulas cannot: at this estimate there
is a **94%** chance of finishing within 300 hours and a **50%** chance within
250. That second number is the one worth putting next to any single-figure
estimate.
