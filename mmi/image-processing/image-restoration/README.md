# Image restoration

Restoration is not enhancement. Enhancement makes an image look better by any
means; restoration assumes a model of the damage and inverts it. The model is
`g = h * f + n`: the true image convolved with a blur, plus noise.

## The inverse filter is exact, and useless

Without noise, dividing by the blur's spectrum recovers the original:

| blur | blurred | after the inverse filter |
|---|---|---|
| Gaussian sigma 1.5 | 20.20 dB | **208.72 dB** |
| motion, 7 pixels | 22.14 dB | infinite |

Add the faintest noise and it collapses:

| noise sigma | blurred | inverse | pseudo-inverse | Wiener |
|---|---|---|---|---|
| 0.000 | 20.20 | 208.72 | 22.79 | 27.72 |
| 0.001 | 20.20 | **-54.34** | 22.78 | 24.13 |
| 0.010 | 20.13 | **-74.34** | 22.44 | 22.51 |
| 0.050 | 19.09 | **-88.32** | 18.27 | 17.76 |

in dB PSNR. The output range shows what "-74 dB" means concretely: for an
original spanning `[0.20, 1.00]`, the restored image spans `[-2.0, 3.2]` at
noise 1e-6, `[-242, 263]` at 1e-4, and `[-24264, 26230]` at 1e-2.

The reason is in the transfer function. The Gaussian's smallest response over a
32 x 32 grid is 2.18e-07, so the division multiplies whatever noise sits at
that frequency by nearly five million.

## The Wiener filter is the inverse filter with the noise accounted for

Multiply by `conj(H) / (|H|^2 + K)` instead of dividing by `H`. Where the blur
is strong it behaves like the inverse filter; where the blur destroyed the
signal, `K` dominates and the gain goes to zero instead of to infinity.

Setting `K = 0` reproduces the plain inverse filter to **3.64e-12**, which is
the sense in which it is the same filter. Sweeping it on an image blurred and
corrupted at sigma 0.01, PSNR 20.20 dB:

| K | PSNR |
|---|---|
| 0 | -74.32 |
| 1e-8 | -25.80 |
| 1e-5 | 3.90 |
| 1e-3 | 21.14 |
| **1e-2** | **22.55** |
| 1e-1 | 20.40 |
| 1.0 | 12.70 |

Fifteen orders of magnitude of `K` span a hundred dB of quality, and the
optimum is a broad plateau rather than a point, which is why the parameter is
usually estimated roughly and left alone.

## Some information is genuinely gone

A motion blur's transfer function is a sinc, and on a sampled image its zeros
land on real frequencies exactly when the blur length divides the image width:

| blur length on a 32-wide image | smallest response | exact zeros |
|---|---|---|
| 5 | 2.05e-02 | none |
| 7 | 1.81e-02 | none |
| 8 | 0.00e+00 | k = 4, 8, 12, 16, 20, 24, 28 |
| 16 | 0.00e+00 | every even k |

Where the response is zero, no filter recovers anything. Division by zero has
no answer, and that is a fact about the blur, not about the algorithm.

On the length-7 motion blur with noise 0.005, blurred at 22.12 dB: the inverse
filter gives 21.69, the pseudo-inverse 28.49 and Wiener 28.61.
