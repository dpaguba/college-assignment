# Quantisation

Sampling discretises the domain, quantisation discretises the range. Both are
needed to get a continuous signal into memory, and both throw information away
permanently.

With uniform steps the worst-case error is half a step, so `n` bits give a
signal-to-noise ratio of about `6n` dB. The measurements confirm it exactly:
2, 4, 8, 16 and 256 levels give 6.0, 12.0, 18.1, 24.1 and 48.2 dB, and worst
errors of 0.5, 0.167, 0.071, 0.033 and 0.002.

## Why logarithmic quantisation exists

Perception of brightness and loudness is roughly logarithmic, so uniform steps
waste precision at the bright end where the eye cannot see the difference, and
starve the dark end where it can. `logarithmic_quantise` puts the fine steps
where they are noticed. This is the same reasoning behind gamma encoding in
[colour-models](../colour-models/), arrived at from the signal side.

## Mach bands

`mach_band_demo` shows why 8 bits per channel is not always enough. At the
boundary between two quantisation levels the eye enhances the edge, so a
gradient posterised to 4 levels shows visible bands at positions 3, 8 and 13
even though every step is the same small size. The steps are not too large in
absolute terms, they are too large next to each other, which is what
[dithering](../dithering/) breaks up.
