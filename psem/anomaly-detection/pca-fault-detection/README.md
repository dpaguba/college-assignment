# Faulty sensors through principal components

Dunia, Qin, Edgar and McAvoy, AIChE Journal 1996, which is the paper whose PDF
in this folder cannot be read as text.

Four sensors driven by two hidden quantities, so the measurements are strongly
correlated and two components suffice. Each measurement is projected onto the
principal subspace and back; the squared residual is what the paper calls Q or
SPE. Normal measurements lie almost in the subspace, so the residual is small;
a sensor fault breaks the correlation and the residual grows.

The eigen-decomposition is done with Jacobi rotations, needing nothing beyond
the standard library, and checked two ways: every eigenpair satisfies
Av = λv, and the eigenvectors are orthonormal.

## Detection works far below the limits

| | residual |
|---|---:|
| largest when healthy | 0.035 |
| offset of 0.5 on one sensor | 0.096 |
| offset of 1.0 | 0.326 |

The faulted value stays well inside the sensor's own observed range, so no
limit check would see it. That is exactly the case the paper is about: the
reading is normal for itself and no longer fits the others.

## Identification does not

Of the four sensors, faults on two are attributed correctly and two are
blamed on their partner. The reason is in the data: sensor 1 measures twice
sensor 0, so a fault on either points the same way in the residual space, and
sensors 2 and 3 are related the same way through the second hidden quantity.

This is not a defect of the computation but the identifiability condition of
the paper: two faults are distinguishable only when their directions in the
residual space differ. With four sensors and two components the residual space
is two-dimensional, and four directions do not fit into it distinguishably.

Detection needs redundancy; identification needs distinguishable directions.
A system can do the first perfectly and the second not at all, and this one
does.
