# Image processing

Operations on an image after it exists, as opposed to the pipeline that
produced it.

| Topic | Question |
|---|---|
| [convolution](convolution/) | the operation almost every filter is |
| [fourier-transform](fourier-transform/) | the same operations seen as frequencies |
| [edge-detection](edge-detection/) | where the image changes fast |
| [image-restoration](image-restoration/) | undoing a known degradation |

## The one idea

Convolution in space is multiplication in frequency. Everything in this block
is that sentence applied: a blur is an attenuation of high frequencies, a
sharpen is their amplification, an edge detector is a high-pass followed by a
decision, and a restoration is a division that fails exactly where the
attenuation was total.

It also explains the failures. A box blur rings because its transform
oscillates. An inverse filter explodes because it divides by numbers near zero.
A midpoint-interpolated contour never converges because its error is
systematic rather than proportional to the sampling.
