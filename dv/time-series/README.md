# Time-dependent data

Decomposition into trend, season and residual; exponential smoothing and what
it lags behind; the discrete Fourier transform with the sampling theorem and
the low-pass filter; polynomial interpolation with the Runge phenomenon; and
splines.

The decomposition is measured against a series with a known trend and season,
the transform against numpy, the smoothing against its own closed form, and
the interpolation against numpy's fit.
