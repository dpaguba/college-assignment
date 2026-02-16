# Lighting

Local illumination: the brightness at a point from the point, the light and the
camera, and nothing else. It cannot produce shadows or reflections, because it
never asks about the rest of the scene. What it gets in return is a constant
cost per pixel, which is what made real-time graphics possible.

## The three terms

Diffuse is the only one with a derivation. A beam arriving at an angle spreads
over a larger patch, so the brightness is the cosine of the incidence angle,
and `lambert` reproduces it to the digit: 1.0000, 0.8660, 0.7071, 0.5000 at 0,
30, 45 and 60 degrees, and 0 beyond 90 rather than negative.

Specular is a fitted function, not physics. Ambient is a constant standing in
for everything the model cannot compute.

## Phong against Blinn

The half vector version is cheaper (no reflection computation, and for a
distant light and viewer it is constant over the surface) and matches at about
four times the exponent: at 5, 10 and 20 degrees off the peak, Phong with
exponent 32 gives 0.885, 0.613, 0.137 and Blinn with 128 gives 0.885, 0.614,
0.141.

The difference shows up at grazing angles, and it is the reason for the
substitution. Measuring the half-width of the highlight along and across the
plane of incidence:

| view elevation | Phong elongation | Blinn elongation |
|---|---|---|
| 40° | 0.77 | 1.19 |
| 15° | 0.97 | 3.72 |
| 6° | 0.99 | 9.48 |

Phong's highlight stays round however oblique the view. Blinn's stretches out
along the surface by a factor of nearly ten at 6 degrees, which is what a real
rough surface does.

## Gouraud against Phong shading

Shade at the vertices and interpolate, or interpolate the normals and shade per
pixel. On a triangle whose vertex normals are splayed as a coarse sphere
approximation would splay them, the two agree exactly at the vertices, by
construction, and disagree by **0.4162 out of about 0.66** at the centroid.

That gap is the highlight. Gouraud cannot represent anything the vertices did
not sample, so a specular highlight smaller than a triangle either vanishes or
smears across the whole face as the object turns.

## Verified

`reflect` preserves length and the angle to the normal to 1.55e-15 over 500
random configurations. `face_normal` flips sign with the vertex order, which is
the same information `back_facing` in [clipping](../clipping/) uses.
