# Image gradients

The two Sobel masks from the slide, applied by cross-correlation:

```
Sh = [[-1,-2,-1],[0,0,0],[1,2,1]]      Sv = [[-1,0,1],[-2,0,2],[-1,0,1]]
Gx = I ⋆ Sv,  Gy = I ⋆ Sh
Gmag = √(Gx² + Gy²),  Gdir = arctan(Gy/Gx)
```

Verified against an analytic answer: on a plane `I = a·x + b·y + c` the Sobel
response is exactly `Gx = 8a` and `Gy = 8b` at every interior pixel, over 50
random planes. On a step edge the magnitude peaks on the edge and the
direction reads 0° for a vertical edge and 90° for a horizontal one.

## Correlation is not convolution

Convolution mirrors the kernel; cross-correlation does not. The Sobel masks
are antisymmetric, so the two differ by a sign: on the same ramp, +8 against
−8, which is a gradient pointing the opposite way.

The mistake survives testing because it is invisible in the magnitude. Only
the direction shows it, and only if someone looks.

## Why gradients and not grey values

A document image is almost nothing but edges, and the direction and strength
of those edges carry the shape of the letters. The grey value carries the
paper, the ink and the lighting, which change from page to page. Methods built
on gradients survive a change of source; methods built on grey values do not.
