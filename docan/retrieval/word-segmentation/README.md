# Word segmentation

The George Washington dataset is not included, so the page is drawn: six lines
of five words from a vocabulary of eight, each word rotated by up to three
degrees and scaled by up to a tenth, with noise on top. The variation is not
decoration. Without it every image of the same word would be identical and
every retrieval score below would be 1.0.

Drawing the page has one advantage over having it: the ground truth is known
rather than estimated, and every segmentation can be held against it exactly.

## Otsu, twice

The threshold is computed once over the running sums of the histogram, and
once by trying all 256 thresholds and taking the one that maximises the
between-class variance. The first is fast and unreadable, the second is slow
and reads like the definition. They agree, and that agreement is the test.

## The result

All 30 words are found, and the tightest box against the drawn one has an
intersection over union of **1.000**. Six lines, six line boxes, no overlap.

## The gap is the whole method

| gap in columns | words found |
|---:|---:|
| 2 | 56 |
| 6 to 30 | **30** |
| 45 and above | 6 |

Below the working range the words fall apart into letter groups, above it the
neighbours merge and each line becomes one word. The range that works is wide
here because the page is printed. On a handwriting where the space between
words is no larger than the space between letters, the range closes, and the
method has nothing left to stand on.

That is the real limit of projection profiles: they assume horizontal,
separated lines and a gap that separates. Where the assumption holds they are
exact and cost nothing; where it does not, no parameter saves them.
