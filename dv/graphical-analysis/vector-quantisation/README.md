# Vector quantisation

Reduce a set of colours to a palette. The median cut repeatedly splits the
box with the largest extent at the median along its widest axis; each
resulting cell contributes its mean.

Doubling the palette lowers the error, which is checked on 20 random colour
sets for palettes of 2, 4 and 8.

## Adaptive against uniform

On colours that clump in two corners of the cube, the median cut puts its
palette entries where the colours are; a uniform grid of four greys spreads
them evenly through a space that is mostly empty. The measured error is far
lower for the median cut, which is the argument for computing a palette
rather than fixing one.

The hyper-octree is the other route: split on the leading bits of the
channels, which needs no sorting and no passes over the data, and gives cells
of fixed shape rather than fixed population.
