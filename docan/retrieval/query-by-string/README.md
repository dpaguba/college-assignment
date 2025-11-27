# Query by string

The query is not an image someone found, it is an image drawn from a string.
That is the useful direction: whoever is searching has a word in mind and
rarely a picture of it.

The query is deliberately drawn in a **different** font from the page. Drawing
both from the same file would measure nothing but the fact that the two images
are the same.

## What it costs

| | mAP |
|---|---:|
| query by example | 0.609 |
| query by string | **0.457** |
| chance | 0.125 |

The gap of 0.152 is the price of the font. The gradients of a typeset word lie
differently from those of the page, and the descriptors follow the gradients.

## The blur helps, and then stops helping

| sigma | mAP |
|---:|---:|
| 0.0 | 0.414 |
| 0.5 | 0.432 |
| 1.0 | 0.457 |
| **1.5** | **0.460** |
| 2.0 | 0.453 |
| 3.0 | 0.401 |

A clean curve with an interior maximum: the smoothing brings the sharp edges
of the typeset query closer to the page, and past the peak it starts erasing
the shape it is supposed to match. The project sheet suggests matching the
query to the dataset with a filter and leaves the strength open; the strength
is where the whole effect sits, and it is worth 0.046.
