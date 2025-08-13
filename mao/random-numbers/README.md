# Random numbers

| Topic | |
|---|---|
| [generators](generators/) | three constants and a period |
| [uniformity-tests](uniformity-tests/) | why uniformity is not enough |
| [transformations](transformations/) | inverse, rejection, convolution |
| [variance-reduction](variance-reduction/) | a tighter answer for the same work |

Chapter three. The block's two results are a warning and a technique.

The warning: a stream alternating between two values passes a chi-square test
over two buckets and has a serial correlation of minus one. Testing a
generator for uniformity tests one property out of several.

The technique: antithetic variates cut the variance of an estimate by a
factor of sixteen here without moving the estimate, so the same run length
buys a four times narrower interval.
