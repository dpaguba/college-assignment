# Query by example

Each of the 30 word images on the page is used once as a query, the other 29
are ranked by distance, and a result counts as relevant if it carries the same
word. Representation: dense SIFT on a grid, quantised against a visual
vocabulary of 32 words learned from the page itself, arranged in a two-level
spatial pyramid and normalised to sum one.

| | |
|---|---:|
| mean average precision | **0.609** |
| mean recall | 1.000 |
| chance | 0.097 |

Six times chance, with every relevant image eventually retrieved.

## The pyramid earns its length

| | mAP |
|---|---:|
| plain histogram | 0.577 |
| two-level pyramid | **0.609** |

The gain is 0.032 for four times the length. Whether that is worth it is a
question about the collection, not about the method.

## Cityblock beats cosine here

| measure | mAP |
|---|---:|
| cityblock | **0.635** |
| cosine | 0.609 |
| Euclidean | 0.600 |

The usual advice, cosine for documents, comes from unnormalised term vectors
where the length of the document is the problem. These representations are
already normalised to sum one, so they are probability histograms, and for
histograms the cityblock distance is the natural one: it is the total variation
between two distributions. The advice was right about its own case and was
carried one step too far.

## Why the ground truth is used for the boxes

The project says to segment using the ground truth, and that is the right
order: with the segmentation done separately, a bad ranking is a bad ranking
and not a segmentation error in disguise.
