# Local surrogates

The LIME idea: do not explain the model, replace it near one point with
something simple, and explain that. Here a weighted linear regression over
points drawn around the place of interest, with an exponential kernel.

## What the measurement shows

Fitting the same step function at the same point with three neighbourhood
widths gives slopes of about 5.2, 1.0 and 0.26: they scale inversely with the
width, so the number reported as the explanation is set by the width.

And the goodness of fit is identical in all three, 0.66. So the fit cannot be
used to choose the width. Comparing two explanations therefore requires
knowing which width produced them, and that is almost never written down.

## Against Shapley values

Both have a hidden choice: the surrogate has the width and the sampling
distribution, SHAP has the background. The surrogate is cheap and has no
guarantees; SHAP is expensive and is pinned down by four axioms. Neither
explains why the model is what it is, only what this one answer was made of.
