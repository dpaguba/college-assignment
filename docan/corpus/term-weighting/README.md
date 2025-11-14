# Term weighting

Three schemes on the same matrix.

| Scheme | What it removes | What it leaves |
|---|---|---|
| absolute | nothing | the length of the document |
| relative | the length | every term equally important |
| tf-idf | the length and the common terms | the discriminative ones |

Verified against a computation written without numpy over 300 random
matrices, term by term.

## The variant of idf is not cosmetic

With the plain `log(N/df)`, a term that appears in every document gets weight
zero and disappears. A document made only of such terms becomes the zero
vector, and the cosine distance is not defined for it. With the smoothed
`log(1 + N/df)` the same term keeps a small weight: on a two-document example
the first row reads `0.0, 0.0` under the plain form and `0.3466, 0.3466` under
the smoothed one.

Which form is wanted depends on what follows. For a nearest-neighbour search
under the cosine distance, the zero vector is a defect. For a subspace method
that only needs the directions, dropping the term is exactly right.

## What idf actually says

It is the stopword idea, estimated from the data instead of taken from a
list. A term in many documents separates nothing, which is the same statement
as "the", "a" and "on" carry no subject. The advantage of estimating it is
that it adapts: in a corpus of legal texts, "court" is a stopword, and no
general list says so.
