# Edge detection

An edge is a large derivative, so every detector is a derivative estimator plus
a decision. The hard part is that differentiating amplifies high frequencies
and noise is high frequency, so a naive derivative reports the noise.

## The operators on a clean step

| operator | peak response | position |
|---|---|---|
| Sobel | 4.0000 | columns 19 and 20 |
| Prewitt | 3.0000 | columns 19 and 20 |
| Roberts | 1.4142 | column 20 |

All three place the edge correctly. They differ in how much smoothing they
apply across the edge, which is what decides their noise behaviour: Sobel
weights the direct neighbours twice, Prewitt uniformly, and Roberts, a 2x2
diagonal difference, not at all.

## Why non-maximum suppression sometimes does nothing

A gradient operator responds over several pixels, so an edge comes out as a
ridge. Thinning means keeping only local maxima **along** the gradient.

On a perfect step the two columns either side have exactly equal magnitude,
4.0 and 4.0, so both are local maxima and the ridge stays two pixels wide. This
is not a bug: the edge really does lie exactly between two pixel centres.
Smoothing first breaks the tie, and then the thinning works: a thresholded
gradient gives run widths `[4, 4]` in a row and the suppressed version gives
`[1, 2]`.

Canny at increasing sigma:

| sigma | edge pixels | widest run | share of single-pixel runs |
|---|---|---|---|
| 1.0 | 119 | 2 | 62% |
| 1.5 | 98 | 2 | 69% |
| 2.0 | 88 | 1 | **100%** |

against 0% and a widest run of 4 for a plain gradient threshold.

## One threshold cannot work

A line whose contrast dips to 0.12 in the middle, with scattered noise at 0.25:

| rule | result |
|---|---|
| threshold 0.2 | line breaks in the middle |
| threshold 0.1 | line survives, and so does all the noise |
| hysteresis 0.1 / 0.2 | **60 of 60** line pixels, noise still present but not connected |

Hysteresis uses the high threshold to decide what an edge is and the low one to
decide how far it continues. It is the observation that edges are connected and
noise is not.

## Noise, and what sigma costs

Edge pixels found on a square with a 76-pixel perimeter:

| noise sigma | plain gradient | Canny sigma 1 | Canny sigma 2 |
|---|---|---|---|
| 0.00 | 156 | 119 | 88 |
| 0.15 | 157 | 83 | 83 |
| 0.30 | 222 | 106 | 80 |

Smoothing is not free. On a circle of radius 10, Canny reports a mean edge
radius of 10.32 at sigma 0.8 and **11.64** at sigma 3.5: a heavier blur pushes
curved edges outwards, because it averages across the curvature.

## Zero crossings

The second derivative crosses zero where the first peaks, so the Laplacian of
Gaussian locates edges without any thinning step: on the step image the
crossings land at columns 19 and 20.

It needs the smoothing more than the first derivative does. On the same noisy
step, the raw Laplacian gives 1424 zero crossings and the smoothed one 819.
