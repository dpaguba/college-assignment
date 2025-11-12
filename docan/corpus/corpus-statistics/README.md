# Corpus statistics

The Brown corpus is not included with the project, so the module builds one
with its structure: 500 documents in 15 categories, distributed the way Brown
distributes them, from 6 documents in science fiction to 80 in learned. The
text is generated, each document mixing general words with the words of its
category, both drawn along a Zipf curve.

| | |
|---|---:|
| categories | 15 |
| documents | 500 |
| tokens | 133 385 |
| distinct words | 94 |

## The uneven distribution is the first result

Learned holds 80 of the 500 documents, science fiction 6. Anyone who always
answers "learned" is right 16 % of the time without having learned anything,
and a classifier that scores 20 % has barely improved on that. The base rate
is the yardstick, and it comes out of the counting, not out of the method.

## Zipf

Rank times frequency stays near 22 000 over the first ranks: 22 512, 22 240,
22 149, 22 376, 22 800. The ten most frequent words alone make up 65 % of the
whole corpus. That is why removing stopwords is worth so much, and why the
term vectors are dominated by words that say nothing about the subject unless
they are weighted down.

## What the counting settles

The size of the vocabulary fixes the length of every term vector. The
distribution over the categories fixes the base rate. The shape of the
frequency curve decides whether stopwords and weighting are needed at all.
All three are decisions about later steps, and all three are read off here.
