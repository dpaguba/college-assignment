# Convolution

Slide a small kernel over the image; each output pixel is a weighted sum of its
neighbourhood. Blur, sharpen, emboss and the first stage of every edge detector
are the same loop with different weights.

## The kernel sum is the response to a flat image

A blur must sum to 1 or it changes the brightness; a derivative must sum to 0
or a flat region produces a response. Verified: box and Gaussian sum to
1.0000000000, the Laplacian to 0.0000000000, and on a flat image of 0.5 the
blurs return exactly 0.5 while the Laplacian returns exactly 0.

## Separability is free speed, not an approximation

A separable `k x k` kernel is two 1D passes: `2k` multiplications per pixel
instead of `k^2`. The results are identical, not approximately equal.

| kernel | multiplications | separated | difference |
|---|---|---|---|
| 3 x 3 | 9 | 6 | 4.44e-16 |
| 9 x 9 | 81 | 18 | 5.55e-16 |
| 15 x 15 | 225 | 30 | 8.88e-16 |

A kernel is separable exactly when its matrix has rank 1. Box and Gaussian have
rank 1; the Laplacian has rank 2 and the emboss kernel rank 3, so neither can
be split.

## Two Gaussians compose into one

Blurring with sigma 1.5 and then 2.0 equals a single blur with
`sqrt(1.5^2 + 2.0^2) = 2.5`, to 5.79e-09. That is the semigroup property, and
it is why a scale-space pyramid can be built incrementally instead of blurring
the original once per level.

## Borders

There is no correct answer outside the image, only trade-offs. On a step image
with a box blur:

| border | left edge | right edge |
|---|---|---|
| zero | 0.0000 | 0.6667 |
| clamp | 0.0000 | 1.0000 |
| wrap | 0.3333 | 0.6667 |
| mirror | 0.0000 | 1.0000 |

Wrapping is the choice the Fourier transform makes, which is why the frequency
domain and the spatial domain agree only under that setting. See
[fourier-transform](../fourier-transform/).

## The median is not a convolution, and that is the point

Being non-linear is what buys robustness. On an image with 80 of 900 pixels set
to pure black or white:

| filter | RMSE against the clean image |
|---|---|
| none | 0.15631 |
| Gaussian 3 x 3 | 0.06810 |
| box 3 x 3 | 0.05919 |
| **median 3 x 3** | **0.01677** |

On Gaussian noise the ranking reverses: 0.04095 for the Gaussian against
0.04508 for the median. Neither filter is better; they assume different noise.

Non-linearity is measurable: over 200 random image pairs,
`median(A+B)` differs from `median(A) + median(B)` by up to **0.6512**, while
the same quantity for convolution is 6.66e-16.
