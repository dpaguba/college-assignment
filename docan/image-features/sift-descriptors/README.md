# SIFT descriptors

The patch is split into cells, each cell gets a histogram of gradient
directions weighted by magnitude, and the histograms are concatenated. Then:
normalise to unit length, clip at 0.2, normalise again.

## The full circle, not the half

The slide gives the direction as `arctan(Gy/Gx)`, which lives in half a
circle. This module uses both signs. In half a circle a rising edge and a
falling edge are the same value, so the left and the right border of a pen
stroke would land in the same bin, and on handwriting that is most of the
signal.

## What the normalisation buys

Unit length removes any uniform change of brightness and contrast, since both
scale every gradient by the same factor. Doubling the contrast or adding a
constant leaves the descriptor unchanged to machine precision, which the tests
check. Clipping bounds the influence of single very strong edges, which can
come from a stain or a tear.

## The clip does not bound what it looks like it bounds

After clipping, the vector is shorter, and dividing by the new length lifts the
largest entries back over the threshold. Measured on the example patch: 0.200
before the second normalisation, **0.266** after it.

So the step bounds the *ratio* between the entries, not their size. Bounding
the size would take alternating clipping and normalising until nothing moves.
The recipe is the published one; the description of what it achieves is the
part that is usually wrong.

## Rotation

The same patch turned by a quarter circle gives a descriptor 1.39 away out of
a possible 2.0. That is intended: a rotated shape is a different shape.
Rotation invariance, where it is wanted, comes from orienting the patch before
describing it, and for text on a page it is not wanted, because the lines run
horizontally anyway.
