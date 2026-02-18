# Rasterisation

Where real numbers meet the pixel grid. Every algorithm here answers the same
question, which pixel centres does this shape cover, and each does it with
integer arithmetic in the inner loop because the decision is a sign test.

## Bresenham

An error term tracked in integers replaces the slope, the multiplication and
the rounding. Against a floating point DDA on 2000 random segments, the two
never differ by more than one pixel, and they differ at all only where the
ideal line passes exactly between two pixel centres.

The algorithm is **not** symmetric: swapping the endpoints gives the same
pixels for 1318 of 2000 random segments and a different tie-break for the rest.
`(0,0)` to `(4,2)` goes through `(1,0)` and `(3,1)`, and the reverse goes
through `(1,1)` and `(3,2)`. Both are equally correct; the ideal line runs
through the corner and something has to choose.

## The fill rule is not a detail

Testing all three edge functions with `>= 0` includes every pixel whose centre
lies on an edge, so two triangles sharing an edge both claim the pixels along
it. On a square split into two triangles, that is 20 pixels claimed twice.

The top-left rule breaks the tie by ownership rather than by geometry: an edge
belongs to the triangle only if it is a top or a left edge. On a 4x4 grid of
cells, each split into two triangles, 32 triangles cover **1600 pixels exactly
once, with 0 double-covered and 0 missed**. Without the rule, every seam in
every mesh is drawn twice, which is invisible on opaque surfaces and an obvious
bright line the moment anything is transparent.

## Barycentric weights belong to the caller's vertex order

A clockwise triangle has to be reordered internally before the edge tests work.
Returning the weights in the internal order rather than the caller's makes
every interpolated attribute of every clockwise triangle wrong, and since about
half the triangles of a mesh are clockwise on screen, the result reads as noise
rather than as a bug. This module reorders them back; reconstructing the pixel
centre from the returned weights is exact to 6.39e-14 for both orientations.

That single mistake was what made the BSP ordering in
[visibility](../visibility/) look broken: the depth interpolated for clockwise
pieces was that of the wrong vertex.

## Perspective-correct interpolation

Screen space linear interpolation is wrong for anything perspective projected.
With vertices at `w = 1` and `w = 10` and a texture coordinate running 0 to 1,
the value halfway across the screen is **0.0909**, not 0.5. Interpolating
`1/w` alongside and dividing at the end recovers it exactly. This is what makes
a floor stretching to the horizon look like a floor.

## Scanline fill and coverage

The scanline fill disagrees with an independent parity test on **0** of 506
cells for a ten-pointed star and 0 of 529 for a U-shaped polygon. Horizontal edges
are skipped and each edge counts for a half-open range, both to keep a shared
vertex from being counted twice.

`coverage` supersamples to get a fraction rather than a yes or no, which is
what anti-aliasing needs: an `n x n` grid gives `n^2 + 1` distinguishable
levels, so 4x4 gives 17.

## Convergence

Pixel counts approach the true area as the triangle grows: 10% error at side
10, 2% at 50, 0.5% at 200, 0.125% at 800. Over 300 random triangles larger than
500 square pixels the worst relative error is 1.79%.
