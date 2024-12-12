# The Fourier transform

An image as a sum of waves. Nothing is lost, the transform is invertible, and
what changes is which questions are easy.

## Verified against the definition

The radix-2 FFT matches the `O(n^2)` definition to 1.93e-13 for lengths 2 to
64, round-trips to 3.23e-15 in one dimension and 8.88e-16 in two, and satisfies
Parseval's theorem to 6.18e-16.

Known transforms come out exactly: a constant gives `X[0] = n` and 0.00e+00
everywhere else, an impulse gives all magnitudes equal to 1, and `cos` at
frequency `k` gives two peaks of height `n/2` at `k` and `n - k`.

## The speedup is the reason the domain is usable

| n | FFT | DFT | speedup | `n^2 / (n log n)` |
|---|---|---|---|---|
| 256 | 0.52 ms | 14.10 ms | 26.9x | 32x |
| 1024 | 2.40 ms | 223.58 ms | 93.3x | 102x |
| 4096 | 10.52 ms | not run | | |

## The convolution theorem, and its one condition

Multiplying spectra reproduces direct convolution to 5.55e-16, but only against
**wraparound** borders:

| border used in the spatial convolution | difference |
|---|---|
| wrap | 3.33e-16 |
| mirror | 0.1064 |
| clamp | 0.1484 |
| zero | 0.2895 |

The frequency domain has no concept of an edge; it always assumes the image
tiles. Every discrepancy between a spatial filter and its frequency-domain
twin is this, and not a bug in either.

## Magnitude is translation invariant, phase is not

Two copies of the same square in different corners have **identical** magnitude
spectra, agreeing to 0.00e+00, while their phase spectra differ by up to
3.1416 radians. Reconstructing from the magnitude of one and the phase of the
other gives back the second image exactly: correlation +1.0000 with the phase
donor and -0.1082 with the magnitude donor.

That is where the structure lives. The magnitude says which frequencies are
present, the phase says where.

## Filtering separates the components exactly

A signal of `0.5 + 0.4 sin(period 8) + 0.1 sin(period 4)` on a 32-wide grid has
its components at `k = 4` and `k = 8`:

| low-pass radius | mean | amplitude at period 8 | at period 4 |
|---|---|---|---|
| 3 | 0.5000 | 0.0000 | 0.0000 |
| 4 | 0.5000 | 0.4000 | 0.0000 |
| 8 | 0.5000 | 0.4000 | 0.1000 |

A high-pass at radius 10 leaves a mean of exactly 0: the zero frequency **is**
the average brightness, which is why a high-passed image looks like an
embossing and not like a photograph.

A component at period 2 is invisible to this grid entirely: `sin(2 pi x / 2)`
is 0 at every integer `x`. That is the Nyquist frequency, and the sampling
theorem in [colour-and-sampling](../../colour-and-sampling/sampling-theorem/)
is the same fact stated in advance.
