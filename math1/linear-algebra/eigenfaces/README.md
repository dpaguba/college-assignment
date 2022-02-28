# Eigenfaces

The application the lecture closes with. A face is a point in a space with one
dimension per pixel, and the principal components are the directions in which
a collection of faces varies most, which are the eigenvectors of its
covariance matrix.

On eight synthetic images built from three underlying patterns:

| components | reconstruction error |
|---|---:|
| 1 | 0.0243 |
| 2 | 0.0073 |
| 3 | 0.00003 |
| 8 | 0 |

The error collapses at three components, and the explained variance says the
same thing: 0.76, 0.17, 0.07, then 0.0001. The data was built from three
patterns, and the method finds three, which is the check that it is measuring
structure rather than noise.

## Why this belongs at the end of the linear algebra

Everything in the pipeline is from the earlier modules. The components are an
orthonormal basis, projecting onto them is a linear map, the coordinates are
coordinates in that basis, and choosing the leading components is choosing a
subspace. The recognition step is a nearest neighbour search in coordinates,
which works here for every stored face.

The compression is the point: 36 pixels reduced to 3 numbers, with an error
of 3 in 100 000, because the data was never really 36-dimensional.
