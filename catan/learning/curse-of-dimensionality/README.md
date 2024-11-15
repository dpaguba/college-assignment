# The curse of dimensionality

Points drawn uniformly in the cube, distances measured from the origin:

| dimension | (farthest − nearest) / nearest |
|---:|---:|
| 1 | 3 315 |
| 2 | 17.9 |
| 10 | 1.41 |
| 100 | **0.27** |

In a hundred dimensions the nearest and the farthest point are within a
quarter of each other. The nearest neighbour stops being a distinction, and
every method built on it inherits the problem.

## Where the volume goes

The unit ball inscribed in the cube, as a share of the cube:

| dimension | 2 | 5 | 10 | 20 |
|---|---:|---:|---:|---:|
| share | 0.785 | 0.164 | 0.0025 | 2 × 10⁻⁸ |

The volume sits in the corners, and a cube has 2^d of them. The volume is
computed twice, once from the Gamma function and once from the recursion
`V_d = (2π/d)·V_{d−2}` starting at 2 and π; the two agree to machine
precision.

The same fact from the practical side: estimating the ball's volume by
sampling 200 000 points in the cube gives 32 654 hits in five dimensions, 465
in ten, and **3** in fifteen. The estimator is not wrong, it has simply run out
of data, and so does every method that needs to fill a space.

Almost all of the volume is also in a thin outer shell: at 99 % of the radius,
the shell holds 3 % of a three-dimensional ball and **87 %** of a
two-hundred-dimensional one.

## What is not cursed

The dimension of the representation is not the dimension of the data. A curve
embedded in a hundred-dimensional space is still a curve: the covariance
matrix here has exactly one eigenvalue above the noise floor, and it carries
essentially all of the variance. Methods that work on the intrinsic dimension
are untouched, which is the whole justification for the subspace step.
