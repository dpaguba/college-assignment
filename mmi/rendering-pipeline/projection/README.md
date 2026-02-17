# Projection

Parallel and perspective projection differ in one row of the matrix. Parallel
leaves `w` at 1, so the divide is a no-op and distance does not change size:
the point `(1,0,z)` maps to `x = 0.5` at `z = -2`, `-10` and `-50` alike.
Perspective copies `-z` into `w`, and the same divide performs the
foreshortening: `x` goes 0.866, 0.433, 0.217, 0.108 as the depth doubles from
2 to 16, exactly halving each time.

Both map into the same cube from -1 to 1, so everything downstream, the
clipper, the rasteriser, the depth test, does not need to know which was used.

## The depth buffer's precision is all in the front

After the divide, depth is a function of `1/z`, and the numbers are worse than
most people expect. With `near = 0.1` and `far = 1000`:

| distance | normalised depth |
|---|---|
| 0.1 | -1.000000 |
| 125.09 | +0.998601 |
| 500.05 | +0.999800 |
| 1000.00 | +1.000000 |

The **midpoint of the depth buffer** sits at distance 0.2. Half of the
available precision covers the first tenth of a unit, and the entire rest of
the scene shares the other half.

That also settles a practical question. Moving the near plane from 1.0 to 0.1
costs far more precision than moving the far plane from 1000 to 10000:

| frustum | share of the buffer spent on the nearer half of the scene |
|---|---|
| near 1.0, far 1000 | 99.90% |
| near 0.1, far 1000 | 99.99% |
| near 1.0, far 10000 | 99.99% |

Depth fighting on distant coplanar surfaces is this table, not a bug.

## The viewport flip

`viewport` negates y, because normalised device coordinates go up and image
rows go down. `(-1,-1)` lands on pixel `(0, 600)` and `(1,1)` on `(800, 0)`.
Getting this wrong produces a correct image upside down, which is why it is
usually found immediately and occasionally not at all.
