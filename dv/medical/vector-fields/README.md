# Vector fields

Streamlines are computed by integrating the field. On the rotation field
(−y, x) the exact orbit is the unit circle, so the distance back to the
starting point after one full turn is the error, and the step size is chosen
as 2π/n so the last step lands exactly where it should.

| steps | Euler | Runge-Kutta |
|---|---|---|
| 628 | 3.19e-2 | 5.25e-10 |

Halving the step size and reading off the exponent gives order 1.04 for Euler
and 4.00 for the classical fourth-order method, which is what the two
promise. Getting that measurement right needed the step to divide 2π exactly:
with a step of 0.01 and 628 steps the orbit stops short of the start, and the
missing 0.003 of arc swamps the method error and makes Runge-Kutta look
merely ten times better instead of ten million.

## Critical points

The Jacobian classifies them. Real eigenvalues of the same sign give a source
or a sink, opposite signs a saddle; purely imaginary eigenvalues a centre,
complex with a real part a spiral. The classification is derived from the
trace and the determinant and checked against `numpy.linalg.eigvals` on six
matrices covering every case.

## Why arrows are not enough

At a readable spacing of 16 pixels, a 512 × 512 image holds 1024 arrows
against 262144 pixels: the arrow plot shows one value in 256. Line integral
convolution smears noise along the field and uses every pixel, which is why
it shows structure between the arrows that the arrows cannot.
