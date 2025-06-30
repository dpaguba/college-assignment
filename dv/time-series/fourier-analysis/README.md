# Fourier analysis

The transform is written out from the definition, one sum per frequency, and
matches `numpy.fft.fft` to 1e-8 for lengths 3, 5, 8, 13 and 16. The inverse
returns the signal. Parseval's identity holds: the energy is the same in
both domains.

The exercise's signal 0.5 sin(3x) + 0.25 sin(10x) gives peaks at exactly the
frequencies 3 and 10 with amplitudes 0.5 and 0.25.

## The sampling theorem, measured

A 15 Hz sine sampled at 20 Hz appears in the spectrum at 5 Hz. The Nyquist
limit is 10 Hz, the signal is above it, and the frequency that comes back is
the reflection. Sampled at 40 Hz the same signal reads 15 Hz. That is the
answer to how high the rate has to be: above twice the highest frequency
present, and it is the frequency present, not the frequency of interest, that
counts.

## Low pass

Setting the coefficients above the cutoff to zero and transforming back
removes the 0.25 component to 1.5e-15. That is what a low-pass filter is in
the frequency domain: a multiplication by an indicator, where in the spatial
domain it would be a convolution.

The spatial domain shows where something happens, the frequency domain how
fast, and the wavelet transform trades resolution to show both.
