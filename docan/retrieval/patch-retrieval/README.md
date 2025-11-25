# Segmentation-free retrieval

No segmentation. The page is indexed once with a dense grid of 10 395
descriptors, a window the size of the query image is slid across it, and every
position is scored. The maxima are separated from their neighbours, and what
remains is the return list.

| | |
|---|---:|
| windows scored | 5 428 |
| windows after suppression | 1 007 |
| average precision at 50 % overlap | **0.568** |
| chance | 0.020 |
| best overlap achieved | 0.640 |

## One found word is one hit

A window counts as a hit only if it reaches the threshold **and** the word it
covers has not already been claimed by a better-scoring window. Without that
rule, one found word yields several hits, and the list looks better the
coarser the suppression is set. The rule turns the coarseness back into a cost.

## The threshold decides the number more than the method does

| overlap threshold | average precision |
|---:|---:|
| 0.2 | 0.634 |
| 0.3 | 0.634 |
| 0.5 | 0.568 |
| 0.7 | **0.000** |
| 0.8 | **0.000** |

At 0.7 the score collapses to zero, and nothing about the search changed. The
best window in the whole run reaches 0.640, because the window has a fixed
size and moves in steps of eight pixels, so it cannot sit exactly on a word.
The measured quality is a property of the evaluation as much as of the method,
and a number quoted without its threshold says very little.

## What dropping the segmentation is worth

It gives up the assumption that words can be separated by gaps, so it still
works on pages where segmentation fails. It costs thousands of scores instead
of thirty, boxes that only roughly sit on the words, and a whole extra step
that did not exist before.
