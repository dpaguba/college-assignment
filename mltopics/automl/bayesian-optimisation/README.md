# The loop

Fit a model, let the acquisition function propose the next point, measure it,
refit. The first few points are random, because a model fitted to nothing says
nothing.

## Against the baselines, same budget

Twenty-five evaluations of a function whose peak is known to eight digits:

| method | regret |
|---|---:|
| Bayesian optimisation | **0.0000016** |
| grid of the same size | 0.0097 |
| random search | 0.0537 |

Six thousand times closer than the grid and thirty-five thousand times closer
than random search, on the same number of evaluations.

The declared optimum is not taken on trust: the verification recomputes it
over two million points and compares.

## Where the advantage lives

| budget | advantage over random search |
|---:|---:|
| 15 | **0.125** |
| 120 | 0.0017 |

At a large budget random search finds the peak too. That is not a weakness of
the method, it is the statement of what it is for: expensive measurements and
few of them.

## What the model assumes

That nearby settings give similar results. Where that does not hold, the model
predicts nothing useful, the acquisition function searches in the dark, and
the method is worse than random search because it commits to a region.
Categorical parameters are the standard case where it does not hold, and that
is why other models are used there.
