# Bag-of-features and the spatial pyramid

Every descriptor is replaced by its nearest visual word, and the image becomes
a histogram over the vocabulary. It is the bag-of-words representation with
images in place of texts, and it loses the same thing: where in the image the
word stood.

## The pyramid puts part of it back

Level 0 is the plain histogram. Each further level divides the image and
appends the histograms of the cells. The cells of one level sum to the level
above, which is the invariant the tests check.

Two images with the same descriptors in swapped positions have the **same**
histogram and **different** pyramids. For word images that is the difference
between two words built from the same letters in another order, which is
exactly the difference that matters and exactly the one the plain histogram
cannot see.

## What the levels cost

| | |
|---|---|
| length | the sum of the cells: three levels means 21 histograms |
| sparsity | the same descriptors spread over more bins |
| shift | a word half a cell further along fills other bins |

Location information traded against robustness, and the trade gets worse with
every level, which is why two or three levels is where it stops in practice.
