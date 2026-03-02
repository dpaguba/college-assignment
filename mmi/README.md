# Mensch-Maschine-Interaktion

The computer graphics half of the course, as a library. One folder per topic:
an implementation and a README stating what was measured, not what was
intended.

| Block | Topics |
|---|---|
| [colour-and-sampling](colour-and-sampling/) | colour models, the sampling theorem, quantisation, dithering |
| [rendering-pipeline](rendering-pipeline/) | transformations, projection, clipping, rasterisation, visibility, lighting, ray tracing |
| [geometric-modelling](geometric-modelling/) | Bezier curves, B-splines, meshes, marching squares, hulls, triangulation, Delaunay |
| [image-processing](image-processing/) | convolution, the Fourier transform, edge detection, restoration |
| [interaction](interaction/) | Fitts' law, collision detection |

[demos/](demos/) holds the interactive HTML pages written during the course.
They visualise what the library computes, and the two are meant to be read
together: the demo shows de Casteljau stepping through a curve, the module
proves the subdivision reproduces it to 9.77e-15.

## How the modules were checked

Where the course published a solution, the module is checked against it. Where
it did not, against an independent oracle: a brute force implementation, a
second algorithm for the same problem, dense sampling, a Monte Carlo estimate,
or a round trip.

That is not a formality. Seven defects in this library were invisible on
reading and appeared only under measurement:

| Defect | How it surfaced |
|---|---|
| barycentric weights returned in the internal, not the caller's, vertex order | BSP visibility order looked wrong on every camera |
| plane fitted from three collinear vertices of a split polygon | the same investigation |
| Delaunay super triangle 20x too small instead of 1e6x | triangle count off by one on 33 of 300 point sets |
| circumcircle test by distance instead of determinant | ill-conditioned near degenerate triangles |
| flatness measured to the chord line instead of the chord segment | flattening exceeded its tolerance on 6 of 200 curves |
| marching squares case table written for a different edge numbering | contour length diverged with resolution |
| depth precision formula with the sign of the near plane flipped | normalised depth outside `[-1, 1]` |

Three of them passed the obvious correctness test for their own module.

## Two claims that measurement contradicted

Area-weighted vertex normals are the intuitive choice and the worst of the
three tried: on a UV sphere the angle weighting is off by 0.43 to 0.85 degrees
and the area weighting by 2.2 to 6.3. And the Phong-versus-Blinn difference is
not a cutoff at grazing angles, which does not happen, but the shape of the
highlight: at 6 degrees above the surface, Blinn's is stretched along it by a
factor of 9.5 and Phong's stays circular.

Both are documented where they were found rather than where they were expected.
