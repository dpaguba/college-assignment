# Colour models

Six ways of naming the same colour, each built for a different job.

RGB is what the hardware does: three light sources added together. It is
useless for a human picking a colour, because "a bit less blue" is not how
anyone thinks. HSV and HLS keep the same gamut but rotate the coordinates so
that hue, saturation and brightness become separate dials, which is why every
colour picker uses one of them.

CMYK subtracts instead of adding, since ink removes light rather than emitting
it. The conversion here is the naive one with full black generation; real print
uses undercolour removal, which is a business decision about ink cost, not a
colour one.

XYZ and Lab are the device-independent pair. XYZ is the CIE reference space,
Lab is XYZ warped so that equal distances look equally different.

## Why the difference between HSV and HLS matters

Pure red is HSV `(0, 1, 1)` but HLS `(0, 0.5, 1)`. Both are correct: HSV's V is
the largest channel, so a fully saturated colour is at the top of the cone,
while HLS's L is the midpoint between the largest and smallest, so full
saturation sits halfway and white is above it. Mixing the two up gives colours
that are twice as bright as intended.

## Why the gamma step is not optional

`rgb_to_xyz` expands gamma first. Skipping that step is the most common colour
bug there is: sRGB values are stored non-linearly (roughly a 2.2 power law)
because that is where the perceptual precision is needed, and every physical
computation, blending, filtering, lighting, needs linear light.

## Verified

Round trips through HSV, HLS and CMYK return the original to within 1e-15. The
XYZ round trip is 1.63e-06, which is the published matrix rounding, not an
error in the code. The luminance weights 0.213, 0.715, 0.072 sum to 1.0.

Two colour pairs the same RGB distance apart (0.100) are 21.12 and 12.69 apart
in Lab. That gap is the entire argument for Lab: RGB distance says the pairs
are equally different, and the eye disagrees by a factor of nearly two.
