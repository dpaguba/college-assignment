# The optimisers

Six methods on a quadratic bowl whose minimum is known in closed form, so
every one of them can be held against the right answer rather than against
each other.

## Each rule against its published form

One step of each method is recomputed by hand from the starting point and
compared with the module's step: plain descent, Polyak's momentum, Nesterov's
look-ahead gradient, AdaGrad's accumulated squares, RMSProp's decaying
average, and Adam's two moments with bias correction. All six agree.

That check is worth having because a mis-transcribed update rule still
descends, just differently, and the run alone would not show it.

## The step size has a known limit

For a quadratic form, plain gradient descent converges exactly when the step
is below `2/λ_max`. Here `λ_max = 3.08`, so the limit is **0.650**:

| rate | 0.1 | 0.3 | 0.6 | 0.8 | 1.0 |
|---|---|---|---|---|---|
| | converges | converges | converges | **diverges** | **diverges** |

The theory and the measurement agree on which side of 0.65 the break falls.

## Momentum in a narrow valley

With a condition number of 40, plain descent needs **342** steps and momentum
needs **107**. The reason is visible in the signs: the crosswise component of
the gradient alternates and cancels in the accumulated velocity, while the
lengthwise component keeps its sign and adds up.

## Two methods that do not quite stop

AdaGrad needs the largest step size of the six, because it damps its own step
fastest; with the default it is still moving when the others have arrived.
RMSProp settles into a small orbit around the minimum rather than a point,
0.035 away, because its effective step never decays on a deterministic problem.
Neither is a defect; both are what the rules say they do.

## Why the rate has to fall on noisy data

At the minimum the noisy gradient is not zero, only zero on average, so a
fixed step keeps bouncing. Averaged over 20 runs after 4 000 steps:

| | distance to the minimum |
|---|---:|
| fixed rate | 0.161 |
| rate falling as 2/t | **0.020** |
