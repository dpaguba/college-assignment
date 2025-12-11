# Corpus

| Module | Topic |
|---|---|
| [corpus-statistics](corpus-statistics/) | what counting the corpus settles |
| [preprocessing](preprocessing/) | stopwords and the Porter stemmer |
| [bag-of-words](bag-of-words/) | vocabulary and term vectors |
| [term-weighting](term-weighting/) | absolute, relative, tf-idf |

The Brown corpus is not part of the material, so the block builds one with its
structure: 500 documents in 15 categories, distributed as Brown distributes
them. The ten most frequent words make up 65 % of it, which is the reason the
next three modules exist at all.

The stemmer is the full published algorithm, checked against 42 of the word
pairs Porter published with it.
