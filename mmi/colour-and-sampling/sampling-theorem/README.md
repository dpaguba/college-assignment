# The sampling theorem

A signal band-limited to `f_max` is fully determined by samples taken at any
rate above `2 f_max`, and can be reconstructed exactly. Below that rate the
information is not merely degraded, it is gone: two different signals produce
the same samples, and nothing downstream can tell them apart.

`reconstruct` implements the Whittaker-Shannon interpolation directly, a sum of
sinc functions centred on the samples. It is the exact reconstruction, and also
the reason nobody uses it: the sinc has infinite support, so every output value
depends on every sample.

## What aliasing actually is

Sampling a 900 Hz sine at 1000 Hz gives samples that are numerically identical,
up to sign, to those of a 100 Hz sine. `dominant_frequency` on the spectrum
reports 100 Hz, and the reconstruction error against the true signal is 1.999,
which is the full amplitude range. The high frequency did not blur, it became a
low frequency.

This is why anti-aliasing has to happen **before** sampling. A filter applied
afterwards is operating on a signal that already contains the wrong frequency
and has no way of knowing it does not belong.

## In graphics

The same theorem explains jagged edges, moire on checkerboard textures and
wagon wheels turning backwards on film. An edge is a step, a step has unbounded
spectrum, so no pixel rate is ever high enough, which is why the fix is
supersampling and filtering rather than more resolution.
