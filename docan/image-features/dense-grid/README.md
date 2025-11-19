# The dense grid

Descriptors at the points of a regular grid, starting far enough inside that
every window lies wholly in the image, so nothing has to be padded at the
border.

On a 384 × 1000 page with step 6 and window 12 that is 10 395 points. Each
pixel falls inside 4 windows, `(12/6)²`, except at the border where the count
drops to zero.

## Why not interest points

Detectors look for corners and blobs. Handwriting is strokes of similar
weight and offers few of either, and the ones it offers are unstable: two
images of the same word would give different point sets, and the two
representations would no longer be comparable.

A fixed grid gives every image the same number of descriptors at comparable
places. The price is that empty places get described too, and they return the
zero vector.

## Overlap is the point

With a step smaller than the window, the windows overlap and every pixel
enters the representation several times. That is the usual setting, and it is
why a finer grid gives not only more descriptors but steadier ones: a small
shift of the image moves each window a little instead of moving one window out
of the picture.
