# Fachprojekt Dokumentenanalyse

Twenty-two modules along the two halves of the course: the semantic analysis
of machine-readable text, and the visual analysis of document images. Both
halves end in the same representation, a histogram over a vocabulary, and the
second half then does with it what the first cannot: find a word on a page
nobody has transcribed.

| Block | Modules | What it holds |
|---|---:|---|
| [corpus](corpus/) | 4 | statistics, stemming, bag-of-words, weighting |
| [classification](classification/) | 4 | distances, k neighbours, validation, naive Bayes |
| [subspaces](subspaces/) | 4 | covariance, reduction, topic space, the equivalence |
| [image-features](image-features/) | 5 | gradients, SIFT, grid, Lloyd, bag-of-features |
| [retrieval](retrieval/) | 5 | segmentation, three searches, evaluation |

## What is missing and what was done about it

The material is two PDFs: 56 slides and four pages on connecting to the
exercise server. The notebooks, the NLTK corpora, the George Washington pages
and the IAM database are all elsewhere. In this environment there is numpy and
Pillow; scipy is broken against numpy 2 and scikit-learn and NLTK are not
installed.

So everything is written from scratch, and the data are generated with their
ground truth known in advance. That turns out to be the better arrangement for
checking: a drawn page has exact word boxes, and a synthetic corpus has exact
counts.

## The slide reproduced exactly

Slide 47 gives an average precision of 0.56 for the list
`[1,0,1,1,1,0,1,0,0,0,1,1,0,0,1]` with 10 relevant items in the dataset. The
module returns 0.5593073593, which is
`(1 + 2/3 + 3/4 + 4/5 + 5/7 + 6/11 + 7/12 + 8/15)/10`, and it is checked
against the area under the precision-recall curve computed independently over
500 random lists.

## Five things the slides leave out

**The equivalence on slide 25 needs the mean subtracted.** The decomposition
of the term-document matrix does correspond to the eigen-analysis of `Σ fᵢfᵢᵀ`,
always. Setting that next to the covariance matrix is only correct for
mean-free data, and term vectors are never mean-free because frequencies are
not negative. Without centring, the first axis points at the mean.

**The 50 % overlap threshold has two readings.** A window containing the whole
word and three times too large scores 0.33 as intersection over union and 1.00
as intersection over the ground truth. One reading calls it relevant, the other
does not, and the mAP differs accordingly.

**The clip in the SIFT descriptor does not bound what it appears to.**
Clipping at 0.2 and normalising again lifts the largest entry to 0.266. The
step bounds the ratio between the entries, not their size.

**Cross-correlation and convolution differ by a sign here.** The Sobel masks
are antisymmetric, so the gradient points the opposite way, and the magnitude
hides it completely.

**Half a circle of gradient direction is not enough for handwriting.** The
`arctan(Gy/Gx)` of the slide cannot separate a rising from a falling edge, so
the two sides of a pen stroke fall in the same bin. The descriptor here uses
the full circle.

## Numbers worth keeping

The word search on the drawn page reaches a mean average precision of **0.609**
against a chance level of 0.097 with an image as the query, and **0.457** with
a word drawn from a string in a different font. The 0.152 between them is the
cost of the font, and blurring the query recovers 0.046 of it at sigma 1.5,
past which the blur starts erasing the shape it should match.

The segmentation-free search scores **0.568** at a 50 % overlap threshold and
**0.000** at 70 %, with nothing about the search changed: the best window in
the run reaches 0.640, because a fixed window moving in steps of eight cannot
sit exactly on a word.

Choosing k on the validation data gives an error rate of 0.442 on data that
carry no signal whatsoever. On fresh data the same k gives 0.500. That is the
sentence on slide 15, made into a number.
