# Bloom filters

Several hash functions set bits; a lookup checks them all. A member always
passes and a non-member passes only if all of its bits were set by others.

With 1024 bits, 50 items and 4 hash functions the predicted false positive
rate is 0.001, and the measured rate over ten thousand non-members agrees.
The optimal number of hash functions for 1024 bits and 100 items is 7.

There are no false negatives, ever, which the module checks by looking up
every inserted item. That asymmetry is what makes the filter usable as a
pre-filter in a star join: a row the filter rejects is certainly not a match,
so it can be discarded without a second thought, and the few that pass
wrongly are removed by the join itself.
