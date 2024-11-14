# Bias and variance

Many samples from the same source, a polynomial fitted on each, and three
quantities measured at every test point: how far the average prediction is
from the truth, how much the predictions scatter around their own average, and
how much the observations themselves are noisy.

The three must add to the expected squared error. That is an identity, not an
approximation, and it is the check on the whole computation. It holds here to
six decimals.

| degree | bias² | variance |
|---:|---:|---:|
| 0 | 0.7266 | 0.0431 |
| 1 | 0.4903 | 0.0657 |
| 3 | 0.0907 | 0.0940 |
| 5 | 0.0038 | 0.2989 |

Bias falls, variance rises, and the sum has its minimum in between. On this
data the best degree is 3.

## Where the picture on the slide stops holding

It holds while the sample still supports the fit. With 25 points and degree 11
it does not:

| degree | bias² | variance |
|---:|---:|---:|
| 8 | 0.007 | 58.8 |
| 11 | **2 793** | 758 222 |
| 14 | 10 458 143 | 1 932 869 190 |

Bias now rises with complexity instead of falling. The individual fits swing so
far at the edges of the range that even their average is nowhere near the
truth. This is not a numerical artefact of the basis: the same figures come out
with an orthogonal polynomial basis, because `lstsq` solves both by singular
value decomposition.

So the neat curve is a statement about the region where the estimator is
determined by the data. Outside it the decomposition still holds as an
identity, and its two halves stop meaning what the picture says they mean.

## What it cannot give you

It needs the true function and many samples from the same source. In practice
there is one sample and the truth is what is being looked for. The
decomposition explains why a middling complexity wins; it does not say which
one. For that there is only measurement on held-out data.
