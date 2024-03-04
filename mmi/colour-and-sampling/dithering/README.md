# Dithering

Quantising a gradient to few levels produces bands. Dithering trades spatial
resolution for colour resolution: every pixel becomes more wrong, and the
average over a small area becomes right. The eye integrates, and the banding
disappears.

The lecture splits the problem in two, and the module follows the split.

## Which colours: median cut

Put every colour of the image into one box, then repeatedly split the box with
the longest side at the **median** along that side. The palette is the average
of each box.

Two choices carry the whole algorithm. Splitting at the median rather than the
midpoint makes it adaptive: in a test set of 800 colours, three quarters of
them bluish, the palette entries go where the colours actually are rather than
spreading evenly over the cube. Splitting the longest side keeps boxes from
degenerating into slabs, which is what a fixed channel order produces.

## Which of them per pixel: ordered vs error diffusion

Ordered dithering compares each pixel against a threshold that depends on its
position (the Bayer matrix). It carries no state, so it is parallel and fast,
and it leaves a visible crosshatch.

Floyd-Steinberg pushes the rounding error on to the neighbours not yet visited,
in the proportions 7, 3, 5, 1 out of 16. The local average then matches the
original exactly, which is why it looks better on photographs. The cost is that
it is strictly sequential.

## The metric that shows the trade

Per pixel, dithering is worse than plain quantisation, and it has to be:

| 4 levels | per pixel | over 4x4 blocks |
|---|---|---|
| plain quantisation | 0.0806 | 0.0470 |
| ordered | 0.1079 | 0.0135 |
| Floyd-Steinberg | 0.1017 | 0.0104 |

A per-pixel metric says dithering made the image worse by a third. The block
metric, which is the one matching what the eye does, says it made it four times
better. Choosing the wrong metric here would reject the correct algorithm.

The interactive demo in [demos/median_cut_algorithm_strict.html](../../demos/median_cut_algorithm_strict.html)
shows the box splitting step by step.
